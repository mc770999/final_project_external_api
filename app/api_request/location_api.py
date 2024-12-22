import os
import requests
from dotenv import load_dotenv
load_dotenv(verbose=True)

def get_location_url(location: str):
    return f'https://api.opencagedata.com/geocode/v1/json?q={location}&key={os.getenv("GEOCODING_API_KEY")}'


def get_lot_and_lan_for_location(location: str):
    url = get_location_url(location)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                coordinates = data["results"][0]["geometry"]
                return coordinates
            else:
                return None, None
        else:
            raise Exception(f"API Error: {response.status_code}")
    except Exception as e:
        print(e)





