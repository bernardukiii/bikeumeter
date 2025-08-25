from strava_api import get_activities
from geocoder import add_location


def main():
    print('Process started!')
    activities = get_activities()
    
    if activities:
        print('Request came back with activities!')
        # loop through the activities & decode location into address
        for act in activities:
            add_location(act)
    else: 
        print("GET request failed :(")

main()