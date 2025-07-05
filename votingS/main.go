package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/binary"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/streadway/amqp"
)

// Configuración via variables de entorno
var (
	amqpURL         = os.Getenv("AMQP_URL")
	rsaPublicKeyPEM = os.Getenv("RSA_PUB_KEY") // ruta a PEM
)

// Estructuras
 type VoteRequest struct {
	ElectionID string `json:"election_id" binding:"required"`
	Choice     string `json:"choice" binding:"required"`
 }

 type VoteMessage struct {
	ElectionID      string `json:"election_id"`
	EncryptedChoice []byte `json:"encrypted_choice"`
	Timestamp       int64  `json:"timestamp"`
 }

 func main() {
	// Carga clave pública RSA
	rsaPub, err := loadRSAPublic(rsaPublicKeyPEM)
	if err != nil {
		log.Fatalf("Error loading RSA key: %v", err)
	}

	// Conexión AMQP
	conn, err := amqp.Dial(amqpURL)
	if err != nil {
		log.Fatalf("AMQP connection error: %v", err)
	}
	defer conn.Close()
	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("AMQP channel error: %v", err)
	}
	defer ch.Close()

	// Declarar exchange
	err = ch.ExchangeDeclare(
		"votes.exchange", "direct", true, false, false, false, nil,
	)
	if err != nil {
		log.Fatalf("Exchange declare error: %v", err)
	}

	// Gin router
	r := gin.Default()

	// Ruta /vote sin protección
	r.POST("/vote", func(c *gin.Context) {
		var req VoteRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// Cifrar choice
		encChoice, err := encryptChoice(rsaPub, req.Choice)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "encryption failed"})
			return
		}

		vote := VoteMessage{
			ElectionID:      req.ElectionID,
			EncryptedChoice: encChoice,
			Timestamp:       time.Now().Unix(),
		}

		body, _ := json.Marshal(vote)
		routingKey := fmt.Sprintf("election.%s.votes", req.ElectionID)
		err = ch.Publish(
			"votes.exchange", routingKey,
			false, false,
			amqp.Publishing{ContentType: "application/json", Body: body, Timestamp: time.Now()},
		)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "publish failed"})
			return
		}

		c.JSON(http.StatusAccepted, gin.H{"status": "vote published"})
	})

	// Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	r.Run(":" + port)
 }

// Funciones de cifrado
type rsaPublicKey rsa.PublicKey

 func loadRSAPublic(path string) (*rsa.PublicKey, error) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	block, _ := pem.Decode(data)
	if block == nil {
		return nil, fmt.Errorf("failed to parse PEM block")
	}
	pub, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		return nil, err
	}
	return pub.(*rsa.PublicKey), nil
 }

 func encryptChoice(pub *rsa.PublicKey, choice string) ([]byte, error) {
	// AES key
	aesKey := make([]byte, 32)
	rand.Read(aesKey)

	// AES-GCM
	block, _ := aes.NewCipher(aesKey)
	gcm, _ := cipher.NewGCM(block)
	nonce := make([]byte, gcm.NonceSize())
	rand.Read(nonce)
	ct := gcm.Seal(nonce, nonce, []byte(choice), nil)

	// RSA-OAEP encrypt aesKey
	encKey, err := rsa.EncryptOAEP(sha256.New(), rand.Reader, pub, aesKey, nil)
	if err != nil {
		return nil, err
	}

	buf := &bytes.Buffer{}
	binary.Write(buf, binary.BigEndian, int32(len(encKey)))
	buf.Write(encKey)
	buf.Write(ct)
	return buf.Bytes(), nil
 }

