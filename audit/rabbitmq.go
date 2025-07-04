package audit

import (
	"encoding/json"
	"log"

	"github.com/streadway/amqp"
)

// StartRabbitListener conecta y consume de RabbitMQ la cola audit_events
en collectiveVote/audit
func StartRabbitListener(rabbitURL, queue string, handler func(Event) error) error {
	conn, err := amqp.Dial(rabbitURL)
	if err != nil {
		return err
	}
	ch, err := conn.Channel()
	if err != nil {
		return err
	}
	msgs, err := ch.Consume(queue, "", true, false, false, false, nil)
	if err != nil {
		return err
	}
	go func() {
		for d := range msgs {
			var ev Event
			if err := json.Unmarshal(d.Body, &ev); err != nil {
				log.Println("Payload inválido:", err)
				continue
			}
			handler(ev)
		}
	}()
	return nil
}
