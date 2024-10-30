from kafka import KafkaConsumer
import json

# Kafka Consumer for MeetingService
consumer = KafkaConsumer(
    'meeting-events',
    bootstrap_servers=['localhost:9092'],
    group_id='meeting-service-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Meeting Service Consumer started.")
for message in consumer:
    event = message.value
    if event['type'] == 'meeting':  # Filter by message type
        # Process the meeting data
        print("Meeting Service processing:", event['data'])
        # Add business logic to handle the meeting data here
