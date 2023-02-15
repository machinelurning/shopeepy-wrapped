import time

from shopeepy_wrapped.browser_automation.driver_setup import driver


def scroll_action(timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


def confirm_scroll_waiting_time():
    print("Enter waiting time during scrolling. Recommended: 3 seconds.")
    print("A longer wait time might be needed if you have a slow connection.")

    waiting_time = int(input("Wait time: "))

    return waiting_time


def scroll_to_bottom():
    waiting_time = confirm_scroll_waiting_time()

    for i in range(3):
        scroll_action(waiting_time)
