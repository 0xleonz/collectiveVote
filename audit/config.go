package audit

import (
	"os"
)

// LoadConfig carga variables de entorno para collectiveVote/audit
type Config struct {
	DatabaseURL string
	RabbitURL   string
}

func LoadConfig() (*Config, error) {
	cfg := &Config{
		DatabaseURL: os.Getenv("DATABASE_URL"),
		RabbitURL:   os.Getenv("RABBITMQ_URL"),
	}
	return cfg, nil
}
