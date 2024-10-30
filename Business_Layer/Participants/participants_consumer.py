from kafka import KafkaConsumer
import json

# Kafka Consumer for ParticipantService
consumer = KafkaConsumer(
    'meeting-events',
    bootstrap_servers=['localhost:9092'],
    group_id='participant-service-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Participant Service Consumer started.")
for message in consumer:
    event = message.value
    if event['type'] == 'participant':  # Filter by message type
        # Process the participant data
        print("Participant Service processing:", event['data'])
        # Add business logic to handle the participant data here
