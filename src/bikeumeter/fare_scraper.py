import time, statistics
from playwright.sync_api import Page, sync_playwright

def scrape_fare(page: Page):
    page.goto("https://9292.nl/")
    
    time.sleep(1)

    # CLOSE COOKIE POPUP
    cookie_popup_btn = page.get_by_role("button", name="Weigeren")
    cookie_popup_btn.wait_for()
    cookie_popup_btn.click()

    time.sleep(0.5)

    # Expect a title "to contain" a substring.
    # going to have to do it for both english and dutch in case it opens either version
    title = page.title()
    
    if title:
        print('Found page, page title:', title)
        # find input, click on it, and input start address
        from_input = page.get_by_role("combobox", name="van")
        from_input.wait_for()
        from_input.click()

        from_input.type('Ganzenhoef', delay=100)
        time.sleep(0.3)
        # wait for the listbox to appear and click the first option
        first_option = page.get_by_role("option").first
        first_option.wait_for(state="visible")
        first_option.click()

        to_input = page.get_by_role("combobox", name="naar")
        to_input.wait_for()
        to_input.click()
        time.sleep(0.2)
        to_input.type('Rokin 69', delay=100)
        time.sleep(0.8)
        # wait for the listbox to appear and click the first option
        first_option = page.get_by_role("option").first
        first_option.wait_for(state="visible")
        first_option.click()

        # fill in timetable | always 9am
        time_input = page.get_by_role("combobox", name="tijd")
        time_input.wait_for()
        time_input.click()
        time.sleep(0.1)
        time_input.type('09:00', delay=100)
        time.sleep(1)

        # click on the button and trigger the search
        page.get_by_role("button", name="Plan je reis").click()

        # wait for results by waiting for the list items that contain the price
        page.wait_for_selector("span.journeyPrice")

        # get all prices
        prices = page.locator("span.journeyPrice").all_text_contents()

        # clean them (remove €, spaces, and convert to float)
        numeric_prices = []
        for p in prices:
            cleaned = p.replace("€", "").replace(",", ".").strip()
            try:
                numeric_prices.append(float(cleaned))
            except ValueError:
                pass  # skip if something goes wrong

        print("Extracted prices:", numeric_prices)

        if numeric_prices:
            median_price = statistics.median(numeric_prices)
            print("Median price:", median_price)
        else:
            print("Could not find prices :(")
    else:
        print('Could not find title :(')


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    scrape_fare(page)
    browser.close()