from confluent_kafka import Producer
from random import randint
import pandas as pd
from time import sleep
import sys

# Kafka broker and topic settings
BROKER = 'localhost:9092'
TOPIC = 'tweets'

# File path for the CSV file containing data
CSV_FILE = 'imdb.csv'
df = pd.read_csv(CSV_FILE)

# Producer callback function
def delivery_report(err, msg):
    """Callback after the message sent"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Start Kafka producer
try:
    p = Producer({'bootstrap.servers': BROKER})
except Exception as e:
    print(f"ERROR --> {e}")
    sys.exit(1)
    
# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    message = row['review']  #  get data from 'review' column

    print(f">>> Sending message: '{message}'")

    # Send message
    p.produce(TOPIC, value=message.encode('utf-8'), callback=delivery_report)

    # Wait for the messages to send from producer
    p.poll(0)

    #sleep(randint(1,4))
    sleep(1)
