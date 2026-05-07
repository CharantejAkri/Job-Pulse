from playwright.async_api import async_playwright
import asyncio
import random
from app.config import get_settings

settings = get_settings()


async def get_browser(proxy=None):
    playwright = await async_playwright().start()

    browser_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]

    launch_options = {
        "headless": True,
        "args": browser_args,
    }

    if proxy or settings.BRIGHT_DATA_PROXY:
        launch_options["proxy"] = {"server": proxy or settings.BRIGHT_DATA_PROXY}

    browser = await playwright.chromium.launch(**launch_options)

    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )

    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    """)

    return browser, context


async def human_delay(min_seconds=5, max_seconds=10):
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)
