from kafka import KafkaProducer
import json
import random
import string
import time
import uuid

# Configuration Parameters
KAFKA_BROKER = '172.20.111.81:9092'  # Replace with your Kafka broker address
KAFKA_TOPIC = 'meeting-events'        # Kafka topic to send messages to
BATCH_MIN_SIZE = 500
BATCH_MAX_SIZE = 1000
PARTICIPANTS_MIN = 50
PARTICIPANTS_MAX = 100
ATTACHMENTS_MIN = 5
ATTACHMENTS_MAX = 10
ERROR_RATE = 0.2  # 20% of messages will have errors

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retries=5  # Retry sending messages up to 5 times on failure
)

# Function to generate random strings
def random_string(min_len, max_len):
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=length))

# Function to create a meeting message
def create_meeting(meeting_id, title, date_time, location, details):
    meeting = {
        "type": "meeting",
        "data": {
            "meeting_id": meeting_id,
            "title": title,
            "date_time": date_time,
            "location": location,
            "details": details
        }
    }
    return meeting

# Function to create a participant message
def create_participant(participant_id, meeting_id, name, email):
    participant = {
        "type": "participant",
        "data": {
            "participant_id": participant_id,
            "meeting_id": meeting_id,
            "name": name,
            "email": email
        }
    }
    return participant

# Function to create an attachment message
def create_attachment(attachment_id, meeting_id, url):
    attachment = {
        "type": "attachment",
        "data": {
            "attachment_id": attachment_id,
            "meeting_id": meeting_id,
            "url": url
        }
    }
    return attachment

# Functions to inject errors into messages
def inject_meeting_error(message):
    error_type = random.choice(['title_length', 'location_length'])
    if error_type == 'title_length':
        # Meeting Title longer than 2000 characters
        message['data']['title'] = 'A' * 2001
    elif error_type == 'location_length':
        # Meeting Location longer than 2000 characters
        message['data']['location'] = 'B' * 2001

def inject_participant_error(message):
    error_type = random.choice(['email_format', 'name_length'])
    if error_type == 'email_format':
        # Invalid Email Format (missing '@')
        message['data']['email'] = 'invalidemailformat'
    elif error_type == 'name_length':
        # Participant Name longer than 600 characters
        message['data']['name'] = 'C' * 601

def inject_attachment_error(message):
    # Attachment URL does not start with http or https
    message['data']['url'] = 'ftp://invalid-url.com/file.pdf'

# Function to generate a single meeting with its participants and attachments
def generate_meeting_with_details():
    meeting_id = str(uuid.uuid4())
    title = random_string(10, 50)
    date_time = "2024-12-31 10:00 AM"  # Example format
    location = random_string(10, 50)
    details = random_string(100, 200)
    
    meeting_message = create_meeting(meeting_id, title, date_time, location, details)
    
    # Generate participants
    num_participants = random.randint(PARTICIPANTS_MIN, PARTICIPANTS_MAX)
    participant_messages = []
    for _ in range(num_participants):
        participant_id = str(uuid.uuid4())
        name = random_string(5, 10)
        email = f"user{random.randint(1, 100)}@example.com"
        participant = create_participant(participant_id, meeting_id, name, email)
        participant_messages.append(participant)
    
    # Generate attachments
    num_attachments = random.randint(ATTACHMENTS_MIN, ATTACHMENTS_MAX)
    attachment_messages = []
    for _ in range(num_attachments):
        attachment_id = str(uuid.uuid4())
        url = f"http://example.com/file{random.randint(1, 100)}.pdf"
        attachment = create_attachment(attachment_id, meeting_id, url)
        attachment_messages.append(attachment)
    
    return meeting_message, participant_messages, attachment_messages

# Function to send a batch of messages
def send_meeting_batch():
    # Determine batch size
    batch_size = random.randint(BATCH_MIN_SIZE, BATCH_MAX_SIZE)
    
    all_messages = []
    
    print(f"Generating a batch of {batch_size} meetings...")
    
    # Generate all messages for the batch
    for _ in range(batch_size):
        meeting, participants, attachments = generate_meeting_with_details()
        all_messages.append(meeting)
        all_messages.extend(participants)
        all_messages.extend(attachments)
    
    total_messages = len(all_messages)
    num_errors = int(ERROR_RATE * total_messages)
    
    print(f"Total messages in batch: {total_messages}")
    print(f"Number of messages to inject errors: {num_errors}")
    
    # Shuffle the messages to randomize error injection
    random.shuffle(all_messages)
    
    # Select the first num_errors messages to inject errors
    error_messages = all_messages[:num_errors]
    
    for message in error_messages:
        if message['type'] == 'meeting':
            inject_meeting_error(message)
        elif message['type'] == 'participant':
            inject_participant_error(message)
        elif message['type'] == 'attachment':
            inject_attachment_error(message)
    
    # Shuffle again to ensure error messages are distributed
    random.shuffle(all_messages)
    
    # Send all messages to Kafka
    sent_count = 0
    for message in all_messages:
        try:
            producer.send(KAFKA_TOPIC, value=message)
            sent_count += 1
            if sent_count % 10000 == 0:
                print(f"Sent {sent_count} messages...")
        except Exception as e:
            print(f"Failed to send message: {e}")
    
    # Flush to ensure all messages are sent
    producer.flush()
    
    print(f"Batch sent successfully with {num_errors} erroneous messages out of {total_messages} total messages.")

# Main execution
if __name__ == "__main__":
    try:
        start_time = time.time()
        send_meeting_batch()
        end_time = time.time()
        duration = end_time - start_time
        print(f"Batch generation and sending completed in {duration:.2f} seconds.")
    except KeyboardInterrupt:
        print("Producer interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        producer.close()
        print("Kafka producer closed.")
