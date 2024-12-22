from external_api.api_request.location_api import get_lot_and_lan_for_location


def get_lat_lon(country_name):
    try:
        location = get_lot_and_lan_for_location(country_name)
        print(location)
        return {"type": "countries", "lat": location["lat"], "lon": location["lng"]} if location else None
    except Exception as e:
        print(e)

