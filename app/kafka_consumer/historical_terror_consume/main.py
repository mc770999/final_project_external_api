import json
import os
from dotenv import load_dotenv
from kafka import KafkaConsumer

from app.db.repository.elastic_repository import insert_document

load_dotenv(verbose=True)

news_historical_topic = os.environ['NEWS_HISTORICAL_TOPIC']

if __name__ == '__main__':

    consumer = KafkaConsumer(
        news_historical_topic,
        bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',  # Read messages from the beginning
        group_id=f"{news_historical_topic}_group",  # Group ID for the consumer group
    )

    print(f"Listening to topic: {news_historical_topic}")

    # Continuously listen for messages
    for message in consumer:
        key = message.key.decode('utf-8') if message.key else None
        insert_document("historical_terror_attack", message.value)
        print(f"Topic: {news_historical_topic}, Key: {key}, Value: {message.value}")
