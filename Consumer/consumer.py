from kafka import KafkaConsumer
import json
import logging
import os
import signal
import sys
import requests
import re

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
API_BASE_URL = 'http://172.20.149.153:5001'  # Adjust to API Gateway

# Validation function for event data
def validate_event_data(event):
    """Validate the event data for errors before processing."""
    if event.get('type') == 'meeting':
        meeting_data = event.get('data', {})
        if len(meeting_data.get('title', '')) > 2000:
            logger.error("Validation failed: Meeting title exceeds 2000 characters.")
            return False
        if len(meeting_data.get('location', '')) > 2000:
            logger.error("Validation failed: Meeting location exceeds 2000 characters.")
            return False

    elif event.get('type') == 'participant':
        participant_data = event.get('data', {})
        email = participant_data.get('email', '')
        if '@' not in email:
            logger.error("Validation failed: Invalid email format for participant.")
            return False
        if len(participant_data.get('name', '')) > 600:
            logger.error("Validation failed: Participant name exceeds 600 characters.")
            return False

    elif event.get('type') == 'attachment':
        attachment_data = event.get('data', {})
        url = attachment_data.get('url', '')
        if not re.match(r'^(http|https)://', url):
            logger.error("Validation failed: Invalid URL format for attachment.")
            return False

    # If all checks pass, return True
    return True

def process_meeting_event(event_data):
    """Process meeting events based on the event type."""
    try:
        meeting_data = event_data.get('data', {})
        response = requests.post(
            f"{API_BASE_URL}/meeting",
            json={
                'meeting_id': meeting_data.get('meeting_id'),
                'title': meeting_data.get('title'),
                'date_time': meeting_data.get('date_time'),
                'location': meeting_data.get('location'),
                'details': meeting_data.get('details')
            }
        )
        logger.info(f"Created meeting: {response.json()}")
        return True

    except Exception as e:
        logger.error(f"Error processing meeting event: {e}")
        return False

def process_attachment_event(event_data):
    """Process attachment events based on the event type."""
    try:
        attachment_data = event_data.get('data', {})
        response = requests.post(
            f"{API_BASE_URL}/attachment",
            json={
                'attachment_id': attachment_data.get('attachment_id'),
                'meeting_id': attachment_data.get('meeting_id'),
                'url': attachment_data.get('url')
            }
        )
        logger.info(f"Created attachment: {response.json()}")
        return True

    except Exception as e:
        logger.error(f"Error processing attachment event: {e}")
        return False

def process_participant_event(event_data):
    """Process participant events based on the event type."""
    try:
        participant_data = event_data.get('data', {})
        response = requests.post(
            f"{API_BASE_URL}/participant",
            json={
                'participant_id': participant_data.get('participant_id'),
                'meeting_id': participant_data.get('meeting_id'),
                'name': participant_data.get('name'),
                'email': participant_data.get('email')
            }
        )
        logger.info(f"Created participant: {response.json()}")
        return True

    except Exception as e:
        logger.error(f"Error processing participant event: {e}")
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

logger.info("Service Consumer started.")

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

        # Validate event data
        if not validate_event_data(event):
            logger.error("Event validation failed. Skipping processing.")
            continue

        if event.get('type') == 'meeting':
            logger.info(f"Received meeting event: {event}")
            success = process_meeting_event(event)
            if success:
                logger.info("Successfully processed meeting event")
            else:
                logger.error("Failed to process meeting event")
        elif event.get('type') == 'attachment':
            logger.info(f"Received attachment event: {event}")
            success = process_attachment_event(event)
            if success:
                logger.info("Successfully processed attachment event")
            else:
                logger.error("Failed to process attachment event")
        elif event.get('type') == 'participant':
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
