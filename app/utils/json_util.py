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