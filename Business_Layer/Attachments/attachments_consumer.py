from kafka import KafkaConsumer
import json
import logging
import os
import signal
import sys
import requests
from datetime import datetime

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
KAFKA_BROKER = os.getenv('KAFKA_BROKER', '172.20.111.81:9092')
API_BASE_URL = 'http://localhost:5003'  # Adjust to your Flask app's URL

def process_attachment_event(event_data):
    """Process attachment events based on the event type."""
    try:
        event_type = event_data.get('action')
        attachment_data = event_data.get('data', {})
        
        if event_type == 'CREATE':
            response = requests.post(
                f"{API_BASE_URL}/attachment",
                json={
                    'attachment_id': attachment_data.get('attachment_id'),
                    'meeting_id': attachment_data.get('meeting_id'),
                    'url': attachment_data.get('url')
                }
            )
            logger.info(f"Created attachment: {response.json()}")

        else:
            logger.warning(f"Unknown event type: {event_type}")
            
        return True

    except Exception as e:
        logger.error(f"Error processing attachment event: {e}")
        return False

# Kafka Consumer setup
consumer = KafkaConsumer(
    'meeting-events',
    bootstrap_servers=[KAFKA_BROKER],
    group_id='attachments-service-group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

logger.info("Attachment Service Consumer started.")

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
        if event.get('type') == 'attachment':
            logger.info(f"Received attachment event: {event}")
            success = process_attachment_event(event)
            if success:
                logger.info("Successfully processed attachment event")
            else:
                logger.error("Failed to process attachment event")

except Exception as e:
    logger.error(f"Error in consumer: {e}")
finally:
    consumer.close()
    logger.info("Consumer closed.")