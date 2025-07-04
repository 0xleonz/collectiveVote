package audit

import (
	"crypto/sha256"
	"encoding/hex"

	"github.com/cbergoon/merkletree"
)

// makeLeaf crea un contenido para el Merkle tree
func makeLeaf(id int, data []byte) merkletree.Content {
	d := append([]byte(string(id)), data...)
	return AuditLeaf{Data: d}
}

// AuditLeaf implementa merkletree.Content para collectiveVote/audit
type AuditLeaf struct {
	Data []byte
}

func (a AuditLeaf) CalculateHash() ([]byte, error) {
	h := sha256.Sum256(a.Data)
	return h[:], nil
}

func (a AuditLeaf) Equals(other merkletree.Content) (bool, error) {
	return hex.EncodeToString(a.Data) == hex.EncodeToString(other.(AuditLeaf).Data), nil
}

// BuildMerkleRoot construye el árbol y retorna la raíz en hex
func BuildMerkleRoot(contents []merkletree.Content) (string, error) {
	tree, err := merkletree.NewTree(contents)
	if err != nil {
		return "", err
	}
	return hex.EncodeToString(tree.MerkleRoot()), nil
}
