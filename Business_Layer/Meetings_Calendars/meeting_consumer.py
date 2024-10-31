# meeting_consumer.py
from kafka import KafkaConsumer
import json
import logging
import os
import signal
import sys

# Configure Logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Retrieve Kafka broker address from environment variable or use default
KAFKA_BROKER = os.getenv('KAFKA_BROKER', '172.20.111.81:9092')  # Replace with your IP

# Kafka Consumer for MeetingService
consumer = KafkaConsumer(
    'meeting-events',
    bootstrap_servers=[KAFKA_BROKER],
    group_id='meeting-service-group',  # Ensure this group ID is correct
    auto_offset_reset='earliest',      # Start reading from the beginning if no offset is committed
    enable_auto_commit=True,           # Automatically commit offsets
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

logger.info("Meeting Service Consumer started.")

# Graceful shutdown handling
def shutdown(signum, frame):
    logger.info("Shutdown signal received. Closing consumer...")
    consumer.close()
    logger.info("Consumer closed.")
    sys.exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

try:
    for message in consumer:
        event = message.value
        if event.get('type') == 'meeting':  # Safely get 'type'
            # Process the meeting data
            logger.info(f"Meeting Service processing: {event.get('data')}")
            # Add business logic to handle the meeting data here
except Exception as e:
    logger.error(f"Error in consumer: {e}")
finally:
    consumer.close()
    logger.info("Consumer closed.")
