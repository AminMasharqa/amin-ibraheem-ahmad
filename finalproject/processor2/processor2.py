import boto3
import psycopg2
import json
import logging
from botocore.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure SQS connection to ElasticMQ
sqs = boto3.client(
    'sqs',
    region_name='us-west-2',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    endpoint_url='http://elasticmq:9324',
    config=Config(retries={'max_attempts': 0}, connect_timeout=5, read_timeout=60)
)

# Queue URL for the SQS queue created in ElasticMQ
SQS_QUEUE_URL = 'http://elasticmq:9324/000000000000/top30'

# Database connection setup
conn = psycopg2.connect(
    host="db",  # Use the Docker service name
    database="musicdb",
    user="postgres",
    password="password"
)
cursor = conn.cursor()

# Function to process messages from SQS
def process_message(message):
    try:
        # Parse the JSON data from the message
        song_data = json.loads(message['Body'])
        logging.info(f"Processing song: {song_data['title']}")

        # Insert the data into the Postgres database
        cursor.execute(
            """
            INSERT INTO songs (rank, title, artist, distribution_date)
            VALUES (%s, %s, %s, %s)
            """,
            (song_data['rank'], song_data['title'], song_data['artist'], song_data['distribution_date'])
        )
        conn.commit()

        logging.info(f"Song {song_data['title']} inserted into the database.")

    except Exception as e:
        logging.error(f"Error processing message: {e}")

# Polling SQS for messages
def poll_sqs():
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20
        )

        if 'Messages' in response:
            for message in response['Messages']:
                process_message(message)
                # Delete message after processing
                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )
        else:
            logging.info("No messages to process.")

if __name__ == "__main__":
    try:
        logging.info("Starting processor2...")
        poll_sqs()
    except KeyboardInterrupt:
        logging.info("Stopping the processor.")
    finally:
        cursor.close()
        conn.close()
