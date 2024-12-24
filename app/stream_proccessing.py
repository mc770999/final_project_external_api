import json
import os
from dotenv import load_dotenv
import faust
from groq import Groq

def convert_to_event(input_data: dict) -> dict:
    def parse_date(date_str):
        try:
            parts = date_str.split("-")
            return {"day": int(parts[2]), "month": int(parts[1]), "year": int(parts[0])}
        except (IndexError, ValueError):
            return {"day": None, "month": None, "year": None}

    output_data = {
        "event_id": None,
        "num_kill": None,
        "num_wound": None,
        "number_of_casualties_calc": None,
        "date": parse_date(input_data.get("date")),
        "summary": input_data.get("body"),
        "num_preps": None,
        "location": {
            "country": input_data.get("country"),
            "region": input_data.get("continent"),
            "city": input_data.get("city"),
            "lat": input_data.get("country_latitude"),
            "lon": input_data.get("country_longitude"),
        },
        "attack_type": [],
        "target_types": [],
        "group_name": []
    }

    # Return the transformed output
    return output_data

def extract_data_flat(input_data):
    flat_data = {
        "date": input_data["date"],
        "title": input_data["title"],
        "body": input_data["body"]
    }
    flat_data.update(input_data["groq"])
    return flat_data

def post_groq_api(article_content: dict) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                    f"{article_content}\n\n"
                    "This is an article. I want to analyze a few things:\n"
                    "1. In what country did it happen?\n"
                    "2. Classify the article into one of the following categories: general news, historical terror attack, or nowadays terror attack.\n\n"
                    "After analyzing, provide a JSON with the following structure:\n"
                    "{\n"
                    "    \"category\": \"str\",\n"
                    "    \"country\": \"str\",\n"
                    "    \"city\": \"str\",\n"
                    "    \"continent\": \"str\",\n"
                    "    \"country_longitude\": \"int\",\n"
                    "    \"country_latitude\": \"int\",\n"
                    "}\n\n"
                    "Respond with the JSON only, without any extra text."
                ),
            }
        ],
        model="llama3-8b-8192",
    )
    try:
        return json.loads(chat_completion.choices[0].message.content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}")



load_dotenv(verbose=True)


# Faust app for stream processing
app = faust.App(
    'streaming',  # App name
    broker=os.environ['BOOTSTRAP_SERVERS'],  # Kafka broker
    value_serializer='json'  # Message value format
)

print(os.environ['NEWS_TOPIC'])
news_topic = app.topic(os.environ['NEWS_TOPIC'])

news_today_topic = app.topic(os.environ['NEWS_TODAY_TOPIC'])
news_historical_topic = app.topic(os.environ['NEWS_HISTORICAL_TOPIC'])


# Stream processing agent
@app.agent(news_topic)
async def process_person(stream):
    async for event in stream.events():
        # Perform some processing
        print(event.value)

        article_analise = post_groq_api(event.value)

        if article_analise.get("category", None) in ["nowadays terror attack"]:
            article_filtered = extract_data_flat({**event.value, "groq": article_analise})
            event = convert_to_event(article_filtered)
            await news_today_topic.send(value=event)
            print(f"Processed and sent: key: value: {event}, topic: {news_today_topic}")

        elif article_analise.get("category", None) in ["historical terror attack"]:
            article_filtered = extract_data_flat({**event.value, "groq": article_analise})
            event = convert_to_event(article_filtered)
            await news_historical_topic.send(value=event)
            print(f"Processed and sent: key: value: {event}, topic: {news_historical_topic}")

        else:
            print("article is not terror news")


if __name__ == '__main__':
    # Run Faust in one thread
    app.main()

