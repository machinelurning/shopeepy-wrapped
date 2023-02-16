import time

from shopeepy_wrapped.browser.driver_setup import driver


def scroll_action(waiting_time: int) -> None:
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(waiting_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


def scroll_to_bottom(waiting_time: int) -> None:
    for i in range(3):
        scroll_action(waiting_time=waiting_time)
