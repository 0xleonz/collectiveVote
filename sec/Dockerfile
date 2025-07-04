# Build stage
FROM golang:1.20-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o sec ./main.go

# Run stage
FROM alpine:3.18
WORKDIR /root/
COPY --from=build /app/sec .
EXPOSE 8080
CMD ["./sec"]

