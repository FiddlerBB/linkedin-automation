import os
from dotenv import load_dotenv
import asyncio

from logger.logger import Logger
from crawler.async_linkedin_crawler import AsyncLinkedInCrawler
from playwright.async_api import Page, async_playwright
from crawler.agents import get_agent
load_dotenv('../.env')
logger = Logger()


logger.info(f"User name: {os.getenv('EMAIL')}")


async def main():
    user_agent = get_agent()
    logger.info(f"User agent: {user_agent}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
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
        linkedin = AsyncLinkedInCrawler(context)
        await linkedin.login(email=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))
        # await linkedin.search("python", 1)
        task = [asyncio.create_task(linkedin.search("python", page_number)) for page_number in range(1, 5)]
        await asyncio.gather(*task)



if __name__ == "__main__":
    asyncio.run(main())
