from typing import Tuple

from rich import print
from selenium.common.exceptions import TimeoutException

from shopeepy_wrapped.config.core import InvalidCredentials
from shopeepy_wrapped.scrapee.scrapee import scrape_orders
from shopeepy_wrapped.shopee_login.login import login_with_credentials, verification_needed, login_success_watcher, \
    verify_by_email_link, prompt_user_credentials


def main() -> Tuple:
    # Attempt login
    correct_credentials = False
    while not correct_credentials:
        try:
            username = prompt_user_credentials()
            print("Logging in...")
            correct_credentials = login_with_credentials(username=username)
        except InvalidCredentials as e:
            print(e)
            print("\n")
            continue

    # Verify e-mail
    login_success = False
    while not login_success:
        try:
            if verification_needed():
                verify_by_email_link()
                print("Verification by e-mail needed.")
                print("Please open your e-mail and click the link sent by Shopee.\n")
            else:
                print("Verification by e-mail not needed.")

            login_success = login_success_watcher()

        except TimeoutException as e:
            if e == "Maximum retries exceeded.":
                print("Verification by e-mail took too long. Please try again.\n")
                continue
    print("Fetching your Shopee orders...")
    orders = scrape_orders(test=True)


main()
