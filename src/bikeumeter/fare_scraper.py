import time, statistics
from playwright.sync_api import Page

def scrape_fare(page: Page, start, end):
    page.goto("https://9292.nl/")
    time.sleep(1)

    # --- CLOSE COOKIE POPUP ---
    try:
        # First try Dutch ("Weigeren")
        cookie_popup_btn = page.get_by_role("button", name="Weigeren")
        cookie_popup_btn.wait_for(timeout=5000)
        cookie_popup_btn.click()
        print("Closed cookie popup (Weigeren).")
    except:
        try:
            # Fallback to English ("Reject")
            cookie_popup_btn = page.get_by_role("button", name="Reject")
            cookie_popup_btn.wait_for(timeout=5000)
            cookie_popup_btn.click()
            print("Closed cookie popup (Reject).")
        except:
            print("No cookie popup found.")

    time.sleep(0.5)

    # --- CONTINUE WITH TRIP SEARCH ---
    title = page.title()
    median_price = None  # always return something
    
    if title:
        print('Found page, page title:', title)

        # FROM input
        from_input = page.get_by_role("combobox", name="van")
        from_input.wait_for()
        from_input.click()
        from_input.type(start, delay=100)
        time.sleep(0.3)
        first_option = page.get_by_role("option").first
        first_option.wait_for(state="visible")
        first_option.click()

        # TO input
        to_input = page.get_by_role("combobox", name="naar")
        to_input.wait_for()
        to_input.click()
        time.sleep(0.2)
        to_input.type(end, delay=100)
        time.sleep(0.8)
        first_option = page.get_by_role("option").first
        first_option.wait_for(state="visible")
        first_option.click()

        # TIME input (always 09:00)
        time_input = page.get_by_role("combobox", name="tijd")
        time_input.wait_for()
        time_input.click()
        time.sleep(0.1)
        time_input.type('09:00', delay=100)
        time.sleep(1)

        # CLICK "Plan je reis"
        page.get_by_role("button", name="Plan je reis").click()

        # WAIT for prices
        page.wait_for_selector("span.journeyPrice", timeout=15000)
        prices = page.locator("span.journeyPrice").all_text_contents()

        # CLEAN & CONVERT
        numeric_prices = []
        for p in prices:
            cleaned = p.replace("€", "").replace(",", ".").strip()
            try:
                numeric_prices.append(float(cleaned))
            except ValueError:
                pass

        if numeric_prices:
            median_price = statistics.median(numeric_prices)
            print("Median price:", median_price)
        else:
            print("Could not find prices :(")
    else:
        print('Could not find title :(')

    return median_price
