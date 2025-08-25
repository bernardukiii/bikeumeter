from strava_api import get_activities


def main():
    print('running...')
    activities = get_activities()
    if activities:
        print("Activities: ", activities)
    else: 
        print("GET request failed :(")

main()