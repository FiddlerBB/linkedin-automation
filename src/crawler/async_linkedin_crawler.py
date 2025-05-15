from playwright.async_api import Page, async_playwright, BrowserContext, Locator
from logger.logger import Logger
from urllib.parse import quote
from playwright.sync_api import TimeoutError, Error

from asyncio import Semaphore
import random, time
logger = Logger()



class AsyncLinkedInCrawler:
    def __init__(self, context: BrowserContext, semaphore: Semaphore = 1):
        self.context = context
        self.base_url = "https://www.linkedin.com"
        self.semaphore = Semaphore(semaphore)
        self.base_timeout = 60000

    def random_delay(self, min_delay: int = 1000, max_delay: int = 3000):
        delay = random.randint(min_delay, max_delay)
        time.sleep(delay / 1000)


    async def login(self, email: str, password: str):
        logger.info("Logging in to LinkedIn")
        page: Page = await self.context.new_page()

        page.set_default_timeout(60000)
        await page.goto(f"{self.base_url}/login")
        await page.wait_for_timeout(2000)
        await page.mouse.move(500, 500)
        logger.info("Waiting for email input")
        email_input = page.locator("input#username")
        await email_input.wait_for(state="visible", timeout=5000)

        await email_input.click()
        self.random_delay()
        await email_input.type(email, delay=100)
        await page.wait_for_timeout(1000)
        logger.info("Waiting for password input")
        password_input = page.locator("input#password")
        await password_input.click()
        await password_input.type(password, delay=100)
        await page.wait_for_timeout(1000)

        sign_in_button = page.locator("button[type='submit']")
        await sign_in_button.click()
        logger.info("Waiting for login to complete")
        code_input = page.locator("input[name='pin']")
        await page.wait_for_timeout(10000)

        if await code_input.is_visible():
            logger.info("Required verification code")

            await code_input.wait_for(state="visible", timeout=2000)
            logger.info("Verification code input is visible")
            verification_code = input("Enter the verification code: ")
            await code_input.click()
            await code_input.type(verification_code, delay=100)
            await page.wait_for_timeout(5000)
            verify_button = page.locator("button[type='submit']")
            await verify_button.click()
            await page.wait_for_timeout(5000)
        logger.info("Login completed")

    async def search(self, query: str, page_number: int):
        async with self.semaphore:
            encoded_query = quote(query)
            query_url = f"{self.base_url}/search/results/people/?keywords={encoded_query}&page={page_number}"
            logger.info(f"Accessing search URL: {query_url}")
            page = await self.context.new_page()
            await page.goto(query_url)
            logger.info("Waiting for search results to load")
            try:
                await page.wait_for_selector("div[class=search-results-container]", timeout=5000)
                logger.info("Search results loaded successfully")
            except TimeoutError:
                logger.error("Search results failed to load")
                logger.info("Retrying...") 
                await page.reload()

            await page.wait_for_timeout(5000)
            await self.parse_data(page)

    async def parse_data(self, page: Page): 
        people: Page = await page.locator("div[class*='OAtondxktxQincpvxsiVKrSNoKXmcTbaSMI']").all()
        logger.info(f"Number of people found: {len(people)}")
        
        for element in people:
            
            title = await element.locator("div[class*='ZfmtkiFeOMVfGYLnMXuSlxHKDUWYSYro']").inner_text()
            location = await element.locator("div[class*='krYeRjyhmouJPAbMkKIHeoBWDGzIbGs']").inner_text()
            logger.info(f"Name: {title}, Location: {location}")
        self.random_delay(1000, 3000)
            # try:
            #     await page.wait_for_selector("button[data-control-name='all_filters']", timeout=10000)
            #     logger.info("Search results loaded successfully")
            #     return 1
            # except TimeoutError:
            #     logger.error("Search results failed to load")
            #     return 0
