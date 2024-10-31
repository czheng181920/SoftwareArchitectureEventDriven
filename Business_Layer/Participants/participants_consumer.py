from kafka import KafkaConsumer
import json
import logging
import os
import signal
import sys
import requests

# Configure Logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
KAFKA_BROKER = os.getenv('KAFKA_BROKER', '172.20.111.81:9092')
API_BASE_URL = 'http://localhost:5004'  # Update this to the correct service URL

def process_participant_event(event_data):
    """Process participant events based on the event type."""
    try:
        event_type = event_data.get('action')
        participant_data = event_data.get('data', {})
        
        if event_type == 'JOIN':
            response = requests.post(
                f"{API_BASE_URL}/create_participant",
                json={
                    'participant_id': participant_data.get('participant_id'),
                    'meeting_id': participant_data.get('meeting_id'),
                    'name': participant_data.get('name'),
                    'email': participant_data.get('email')
                }
            )
            logger.info(f"Added participant: {response.json()}")

        else:
            logger.warning(f"Unknown event type: {event_type}")
            
        return True

    except Exception as e:
        logger.error(f"Error processing participant event: {e}")
        return False

# Kafka Consumer setup
consumer = KafkaConsumer(
    'meeting-events',
    bootstrap_servers=[KAFKA_BROKER],
    group_id='participants-service-group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

logger.info("Participants Service Consumer started.")

def shutdown(signum, frame):
    logger.info("Shutdown signal received. Closing consumer...")
    consumer.close()
    logger.info("Consumer closed.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

try:
    for message in consumer:
        event = message.value
        if event.get('type') == 'participant':
            logger.info(f"Received participant event: {event}")
            success = process_participant_event(event)
            if success:
                logger.info("Successfully processed participant event")
            else:
                logger.error("Failed to process participant event")

except Exception as e:
    logger.error(f"Error in consumer: {e}")
finally:
    consumer.close()
    logger.info("Consumer closed.")
