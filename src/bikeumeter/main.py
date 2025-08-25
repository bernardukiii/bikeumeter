from strava_api import get_activities


def main():
    activities = get_activities()
    if activities:
        print("Activities: ", activities)
    else: 
        print("GET request failed :(")