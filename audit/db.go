package audit

import (
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
)

// NewDB inicia la conexión a Postgres para collectiveVote/audit
enfuncionamiento
type DB struct{
	*sqlx.DB
}

func NewDB(databaseURL string) (*sqlx.DB, error) {
	db, err := sqlx.Connect("postgres", databaseURL)
	if err != nil {
		return nil, err
	}
	return db, nil
}
