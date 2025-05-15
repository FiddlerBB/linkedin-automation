from playwright.sync_api import Page, sync_playwright
from logger.logger import Logger

from urllib.parse import quote
from playwright.sync_api import TimeoutError, Error
logger = Logger()

class LinkedInCrawler:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://www.linkedin.com"

        self.page.set_default_timeout(60000)

    def login(self, email: str, password: str):
        logger.info("Logging in to LinkedIn")
        self.page.goto(f"{self.base_url}/login")
        self.page.wait_for_timeout(2000)
        self.page.mouse.move(500, 500)
        logger.info("Waiting for email input")
        email_input = self.page.locator("input#username")
        email_input.wait_for(state="visible", timeout=5000)

        email_input.click()
        email_input.type(email, delay=100)
        self.page.wait_for_timeout(1000)
        logger.info("Waiting for password input")
        password_input = self.page.locator("input#password")
        password_input.click()
        password_input.type(password, delay=100)
        self.page.wait_for_timeout(1000)

        sign_in_button = self.page.locator("button[type='submit']")
        sign_in_button.click()
        logger.info("Waiting for login to complete")
        code_input = self.page.locator("input[name='pin']")
        self.page.wait_for_timeout(10000)

        if code_input.is_visible():
            logger.info("Required verification code")

            code_input.wait_for(state="visible", timeout=2000)
            logger.info("Verification code input is visible")
            verification_code = input("Enter the verification code: ")
            code_input.click()
            code_input.type(verification_code, delay=100)
            self.page.wait_for_timeout(5000)
            verify_button = self.page.locator("button[type='submit']")
            verify_button.click()
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(5000)
        logger.info("Login completed")

    def search(self, query: str, page: int = 1):
        encoded_query = quote(query)
        query_url = f"{self.base_url}/search/results/people/?keywords={encoded_query}&page={page}"
        logger.info(f"Accessing search URL: {query_url}")

        self.page.goto(query_url)
        logger.info("Waiting for search results to load")
        self.page.wait_for_selector("div[class=search-results-container]", timeout=5000)

        self.page.wait_for_timeout(2000)
        return self.send_connect_request()

    def send_connect_request(self):
        connect_buttons = self.page.locator("button[type='button']:has-text('Connect')")
        count = connect_buttons.count()
        logger.info(f"Found {count} available connects")
        if count == 0:
            logger.info("No available connects found")
            return 0
        res = 0
        while True:
            connect_button = self.page.locator(
                "button[type='button']:has-text('Connect')"
            ).first
            if not connect_button.is_visible(timeout=1000):
                break
            try:
                connect_button.click()
                self.page.wait_for_timeout(1000)

                send_button = self.page.locator(
                    "button[aria-label='Send without a note']"
                )
                if send_button.is_visible(timeout=1000):
                    send_button.click()
                    res += 1
                    logger.info(f"Sent connection request: {res}")
                else:
                    logger.warning("Send button not found")

                self.page.wait_for_timeout(2000)
            except Error as e:
                logger.error(f"Error sending request: {e}")

        logger.info(f"Sent {res} connect requests")
        return res
