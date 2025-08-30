from strava_api import get_activities
from geocoder import add_location
from spreadsheets import write_activity_to_sheet
from token_flow import refresh_access_token 

def main():
    print('Refreshing tokens...')
    access_token, _ = refresh_access_token() # get token # unpack tupple

    print('Getting activities...')
    activities = get_activities(access_token) # pass the token here where it is used
    
    if activities:
        print('Request came back with activities!')
        # loop through the activities & decode location into address
        for act in activities:
            add_location(act)
        write_activity_to_sheet(activities)
    else: 
        print("GET request failed :(")

main()