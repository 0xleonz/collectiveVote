package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/tuusuario/collectiveVote/audit/internal/audit"
)

func main() {
	// Inicializa auditoría
	aud, err := audit.NewService()
	if err != nil {
		log.Fatalf("Error iniciando servicio de auditoría: %v", err)
	}

	// Setup HTTP
	r := mux.NewRouter()
	audit.RegisterHandlers(r, aud)

	addr := ":8080"
	log.Println("Audit API escuchando en", addr)
	log.Fatal(http.ListenAndServe(addr, r))
}
