import re, time
from playwright.sync_api import Page, expect, sync_playwright

def scrape_fare(page: Page):
    page.goto("https://9292.nl/")
    
    time.sleep(1)

    # Expect a title "to contain" a substring.
    # going to have to do it for both english and dutch in case it opens either version
    title = page.title()

    if re.search("Where do you want to go?", title):
        print('Eng version')
        # find input, click on it, and input start address
        from_input = page.get_by_role("textbox", name="from")
        from_input.wait_for()
        from_input.click()

        from_input.type('Ganzenhoef', delay=100)
        time.sleep(0.1)

        to_input = page.get_by_role("textbox", name="to")
        to_input.wait_for()
        to_input.click()
        time.sleep(0.2)
        to_input.type('Rokin 69', delay=100)
        time.sleep(0.8)

        # fill in timetable | always 9am
        time_input = page.get_by_role("textbox", name="time")
        time_input.wait_for()
        time_input.click()
        time.sleep(0.1)
        time_input.type('09:00', delay=100)
        time.sleep(1)

        # click on the button and trigger the search
        page.get_by_role("button", name="Plan your trip").click()

    elif re.search("Waar wil je heen?", title):
        print('NL version')
        # find input, click on it, and input start address
        from_input = page.get_by_role("textbox", name="from")
        from_input.wait_for()
        from_input.click()

        from_input.type('Ganzenhoef', delay=100)
        time.sleep(0.3)

        to_input = page.get_by_role("textbox", name="to")
        to_input.wait_for()
        to_input.click()
        time.sleep(0.2)
        to_input.type('Rokin 69', delay=100)
        time.sleep(0.8)

        # fill in timetable | always 9am
        time_input = page.get_by_role("textbox", name="time")
        time_input.wait_for()
        time_input.click()
        time.sleep(0.1)
        time_input.type('09:00', delay=100)
        time.sleep(1)

        # click on the button and trigger the search
        page.get_by_role("button", name="Plan je reis").click()
    else:
        print('Could not find title :(')


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    scrape_fare(page)
    time.sleep(10)  # keep browser open to see results
    browser.close()