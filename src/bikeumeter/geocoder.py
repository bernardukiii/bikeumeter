import os
import googlemaps
from dotenv import load_dotenv
import time

load_dotenv()

G_API_KEY = os.environ["G_API_KEY"]
gmaps = googlemaps.Client(key=G_API_KEY)

def add_location(activity):
    # pause to avoid hitting API rate limits
    time.sleep(4)

    start_coords = activity.get('start_latlng')
    end_coords = activity.get('end_latlng')

    # Default values
    activity['start_location'] = "Unknown"
    activity['end_location'] = "Unknown"

    try:
        # Start location
        if start_coords and len(start_coords) == 2:
            start_lat, start_lon = start_coords
            print(f'Geocoding start: {start_lat}, {start_lon}')
            start_result = gmaps.reverse_geocode((start_lat, start_lon))
            if start_result:
                activity['start_location'] = start_result[0]['formatted_address']

        # End location
        if end_coords and len(end_coords) == 2:
            end_lat, end_lon = end_coords
            print(f'Geocoding end: {end_lat}, {end_lon}')
            end_result = gmaps.reverse_geocode((end_lat, end_lon))
            if end_result:
                activity['end_location'] = end_result[0]['formatted_address']

    except Exception as e:
        print("Geocoding error:", e)

    return activity
