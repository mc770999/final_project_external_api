import json
import os
import time

from kafka import KafkaProducer

from external_api.api_request.groq_api import post_groq_api
from external_api.api_request.news_api import fetch_articles
from external_api.service.counter_service import get_counter, increment_counter
from dotenv import load_dotenv

load_dotenv(verbose=True)

if __name__ == '__main__':
    while True:
        counter = get_counter()

        api_articles = fetch_articles(os.getenv("API_NEWS_KEY"), os.getenv("NEWS_API_KEYWORD"), articles_page=counter)

        print(api_articles)
        print(post_groq_api(api_articles["articles"]["results"][0]))

        list(print())

        for article in api_articles["articles"]["results"]:
            kafka_producer = KafkaProducer(
                bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            kafka_producer.send(
                os.getenv("NEWS_TOPIC"),
                value=article,
                key=os.getenv("NEWS_KEY").encode('utf-8')
            )
            kafka_producer.flush()

        increment_counter()

        time.sleep(120)

