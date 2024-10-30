from kafka import KafkaConsumer
import json

# Kafka Consumer for AttachmentService
consumer = KafkaConsumer(
    'meeting-events',
    bootstrap_servers=['localhost:9092'],
    group_id='attachment-service-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Attachment Service Consumer started.")
for message in consumer:
    event = message.value
    if event['type'] == 'attachment':  # Filter by message type
        # Process the attachment data
        print("Attachment Service processing:", event['data'])
        # Add business logic to handle the attachment data here
