import os
from dotenv import load_dotenv

from logger.logger import Logger
from crawler.linkedin_crawler import LinkedInCrawler
from playwright.sync_api import Page, sync_playwright
from crawler.agents import get_agent
load_dotenv('../.env')
logger = Logger()


def main():
    user_agent = get_agent()
    logger.info(f"User agent: {user_agent}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
        user_agent=user_agent,
        locale='vn-VN',
        color_scheme='light',
        timezone_id='Asia/Ho_Chi_Minh',
        permissions=[],
        extra_http_headers={
            "accept-language": "en-US,en;q=0.9",
        },
        
        viewport={"width": 1280, "height": 720}
    )
        page = context.new_page()

        linkedin = LinkedInCrawler(page)
        linkedin.login(email=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))
        total_sent = 0
        for i in range(1, 100):
            sent = linkedin.search("data", page=i)
            total_sent += sent
            logger.info(f"Total sent: {total_sent}")
        logger.info("Finished sending connection requests")

if __name__ == "__main__":
    main()
