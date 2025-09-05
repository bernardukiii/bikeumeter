from strava_api import get_activities
from geocoder import add_location
from spreadsheets import write_activity_to_sheet
from token_flow import refresh_access_token 
from fare_scraper import scrape_fare
from playwright.sync_api import sync_playwright

def main():
    print('Refreshing tokens...')
    access_token, _ = refresh_access_token() # get token # unpack tupple

    print('Getting activities...')
    activities = get_activities(access_token) # pass the token here where it is used
    # reverse order before writing
    activities = list(reversed(activities)) # so it writes them in order to the sheet
    
    if activities:
        print('Request came back with activities!')
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for act in activities:
                # Add location details (assume it sets from_address & to_address on act)
                add_location(act)

                from_addr = act.get("start_location")
                to_addr = act.get("end_location")

                if from_addr and to_addr:
                    try:
                        fare_value = scrape_fare(page, from_addr, to_addr)
                        act["fare"] = fare_value  # store single value (e.g. median)
                    except Exception as e:
                        print(f"Failed to scrape fares for activity {act.get('id')}: {e}")
                        act["fare"] = None
                else:
                    act["fare"] = None

            browser.close()


        write_activity_to_sheet(activities)
    else: 
        print("GET request failed :(")

main()