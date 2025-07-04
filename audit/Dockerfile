# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app

# Cache modules
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build binary
RUN go build -o audit-service ./cmd/audit

# Final stage
FROM alpine:latest
WORKDIR /root/

# Copy the compiled binary
COPY --from=builder /app/audit-service .

# Expose port
EXPOSE 8080

# Run
CMD ["./audit-service"]
