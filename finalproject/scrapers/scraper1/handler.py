from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import boto3
from botocore.config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure SQS connection to ElasticMQ
sqs = boto3.client(
    'sqs',
    region_name='us-west-2',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    endpoint_url='http://elasticmq:9324',  # Use the Docker service name instead of localhost
    config=Config(retries={'max_attempts': 0}, connect_timeout=5, read_timeout=60)
)

# Queue URL for the SQS queue created in ElasticMQ
SQS_QUEUE_URL = 'http://elasticmq:9324/000000000000/youtube_trend_100'

def send_to_sqs(data):
    try:
        response = sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(data))
        logging.info(f"Message sent to SQS with ID: {response['MessageId']}")
    except Exception as e:
        logging.error(f"Failed to send message to SQS: {e}")

# Selenium Chrome setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

try:
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://charts.youtube.com/charts/TopVideos/IL/weekly"
    driver.get(url)
    time.sleep(10)

    # Parse the HTML content
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    songs_data = []
    entries = soup.find_all('ytmc-entry-row')
    if not entries:
        logging.warning("No entries found on the page.")
    else:
        logging.info(f"Found {len(entries)} entries.")
        
    for entry in entries:
        try:
            song = {
                'title': entry.find('div', class_='title').text.strip(),
                'artists': [artist.text.strip() for artist in entry.find_all('span', class_='artistName')],
                'rank': entry.find('span', id='rank').text.strip(),
                'views': entry.find_all('div', class_='metric content center tablet-non-displayed-metric style-scope ytmc-entry-row')[-1].text.strip(),
                'weeks_in_parade': entry.find_all('div', class_='metric content center tablet-non-displayed-metric style-scope ytmc-entry-row')[-2].text.strip()
            }
            logging.info(f"Scraped song: {song}")
            songs_data.append(song)
        except Exception as e:
            logging.error(f"Error processing entry: {e}")

    # Send each song data to SQS
    for song in songs_data:
        send_to_sqs(song)

except Exception as e:
    logging.error(f"An error occurred during scraping: {e}")

finally:
    # Ensure the WebDriver is closed even if an error occurs
    driver.quit()

logging.info("Scraping and sending to SQS completed.")
