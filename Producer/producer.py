# producer.py
from kafka import KafkaProducer
import json
import random
import string
import time

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to generate random strings
def random_string(min_len, max_len):
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to generate a meeting message
# TODO: figure out how we want to structure the message
def create_meeting():
    meeting = {
        "type": "meeting",
        "data": {
            "title": random_string(10, 50),
            "location": random_string(10, 50),
            "participants": [
                {
                    "name": random_string(5, 10),
                    "email": f"user{random.randint(1, 100)}@example.com",
                }
                for _ in range(random.randint(50, 100))
            ],
            "attachments": [
                {
                    "url": f"http://example.com/file{random.randint(1, 100)}.pdf"
                }
                for _ in range(random.randint(5, 10))
            ]
        }
    }
    
    # Introduce errors in 20% of the meetings
    if random.random() < 0.2:
        meeting["data"]["title"] = random_string(2001, 2100)  # Title too long
        meeting["data"]["location"] = random_string(2001, 2100)  # Location too long
        if meeting["data"]["participants"]:
            meeting["data"]["participants"][0]["email"] = "invalidemailformat"  # Invalid email
    
    return meeting

# Function to send a batch of messages
def send_meeting_batch(batch_size=500):
    batch = [create_meeting() for _ in range(batch_size)]
    for meeting in batch:
        producer.send('meeting-events', value=meeting)
    producer.flush()
    print(f"Sent batch of {batch_size} meetings.")

# Main execution
if __name__ == "__main__":
    # try:
    #     while True:
    #         send_meeting_batch()
    #         time.sleep(5)
    # except KeyboardInterrupt:
    #     print("Producer stopped.")
    try:
        send_meeting_batch()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.close()
