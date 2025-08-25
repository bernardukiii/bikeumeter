import os
import googlemaps
from dotenv import load_dotenv

load_dotenv()

G_API_KEY = os.environ.get("G_API_KEY")
gmaps = googlemaps.Client(key=G_API_KEY)

def add_location(activity):
    lat = activity.get('start_latitude')
    lon = activity.get('start_longitude')
    
    if lat is None or lon is None:
        activity['location'] = "Unknown"
        return activity

    try:
        result = gmaps.reverse_geocode((lat, lon))
        if result:
            activity['location'] = result[0]['formatted_address']
        else:
            activity['location'] = "Unknown"
    except Exception as e:
        print("Geocoding error:", e)
        activity['location'] = "Unknown"

    return activity
