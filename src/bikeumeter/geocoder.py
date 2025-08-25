import os
import googlemaps
from dotenv import load_dotenv

load_dotenv()

G_API_KEY = os.environ.get("G_API_KEY")
gmaps = googlemaps.Client(key=G_API_KEY)

def add_location(activity):
    # start
    start_lat = activity.get('start_latitude')
    start_lon = activity.get('start_longitude')
    # end
    end_lat = activity.get('end_latitude')
    end_lon = activity.get('end_longitude')

    # Default
    activity['start_location'] = "Unknown"
    activity['end_location'] = "Unknown"

    try:
        # Start location
        if start_lat and start_lon:
            start_result = gmaps.reverse_geocode((start_lat, start_lon))
            if start_result:
                activity['start_location'] = start_result[0]['formatted_address']
        
        # End location
        if end_lat and end_lon:
            end_result = gmaps.reverse_geocode((end_lat, end_lon))
            if end_result:
                activity['end_location'] = end_result[0]['formatted_address']

    except Exception as e:
        print("Geocoding error:", e)

    return activity
