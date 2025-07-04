package main

import (
    "encoding/json"
    "log"
    "net/http"
    "sync"

    "github.com/google/uuid"
)

// In-memory token store
var tokenStore = struct {
    sync.Mutex
    m map[string]bool
}{m: make(map[string]bool)}

// In-memory vote store
var voteStore = struct {
    sync.Mutex
    votes []string
}{votes: make([]string, 0)}

func main() {
    http.HandleFunc("/issue-token", issueTokenHandler)
    http.HandleFunc("/cast-vote", castVoteHandler)
    http.HandleFunc("/results", resultsHandler)

    log.Println("[sec] Service listening on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}

// issueTokenHandler generates a one-time voting token
func issueTokenHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }
    tok := uuid.New().String()

    tokenStore.Lock()
    tokenStore.m[tok] = true
    tokenStore.Unlock()

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"token": tok})
}

// castVoteHandler accepts an encrypted vote plus token
func castVoteHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req struct {
        Token         string `json:"token"`
        EncryptedVote string `json:"encryptedVote"`
    }
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Bad request", http.StatusBadRequest)
        return
    }

    // validate token
    tokenStore.Lock()
    valid, ok := tokenStore.m[req.Token]
    if !ok || !valid {
        tokenStore.Unlock()
        http.Error(w, "Invalid or used token", http.StatusForbidden)
        return
    }
    tokenStore.m[req.Token] = false
    tokenStore.Unlock()

    // store vote
    voteStore.Lock()
    voteStore.votes = append(voteStore.votes, req.EncryptedVote)
    voteStore.Unlock()

    w.WriteHeader(http.StatusNoContent)
}

// resultsHandler returns all encrypted votes
func resultsHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    voteStore.Lock()
    out := make([]string, len(voteStore.votes))
    copy(out, voteStore.votes)
    voteStore.Unlock()

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string][]string{"encryptedVotes": out})
}

