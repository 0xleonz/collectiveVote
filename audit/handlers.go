package audit

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/jmoiron/sqlx"
)

// Service implementa la lógica de consulta y persistencia
type Service struct {
	DB *sqlx.DB
}

// NewService inicializa DB y RabbitMQ listener
func NewService() (*Service, error) {
	cfg, _ := LoadConfig()
	db, err := NewDB(cfg.DatabaseURL)
	if err != nil {
		return nil, err
	}
	StartRabbitListener(cfg.RabbitURL, "audit_events", func(ev Event) error {
		return insertEvent(db, ev)
	})
	// Aquí podrías iniciar periodic Merkle builder
	return &Service{DB: db}, nil
}

// RegisterHandlers monta las rutas HTTP para collectiveVote/audit
func RegisterHandlers(r *mux.Router, s *Service) {
	r.HandleFunc("/audit/logs", s.handleGetLogs).Methods("GET")
	r.HandleFunc("/audit/root", s.handleGetRoot).Methods("GET")
	r.HandleFunc("/audit/proof", s.handleGetProof).Methods("GET")
}

func (s *Service) handleGetLogs(w http.ResponseWriter, r *http.Request) {
	// Implementar consulta a audit_log
}

func (s *Service) handleGetRoot(w http.ResponseWriter, r *http.Request) {
	// Implementar consulta a últimas merkle_roots
}

func (s *Service) handleGetProof(w http.ResponseWriter, r *http.Request) {
	// Implementar generación de prueba Merkle
}
