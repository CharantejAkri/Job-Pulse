from scraper.base import get_browser, human_delay
import asyncio
from typing import List, Dict, Optional


def scrape_indeed(
    job_title: str, location: Optional[str], date_posted: str
) -> List[Dict]:
    """
    Indeed India scraper.
    Scrapes publicly available job listings only.
    """
    results = []

    async def _scrape():
        browser, context = await get_browser()
        page = await context.new_page()

        try:
            search_url = f"https://in.indeed.com/jobs?q={job_title}"
            if location:
                search_url += f"&l={location}"
            if date_posted == "past_24h":
                search_url += "&fromage=1"

            await page.goto(search_url, wait_until="networkidle")
            await human_delay(5, 8)

            job_cards = await page.query_selector_all(".job_seen_beacon")

            for card in job_cards:
                title_el = await card.query_selector("a[data-jk]")
                company_el = await card.query_selector("[data-testid='company-name']")
                location_el = await card.query_selector("[data-testid='text-location']")
                salary_el = await card.query_selector(
                    "[data-testid='attribute_snippet_testid']"
                )

                if title_el and company_el:
                    results.append(
                        {
                            "job_title": (
                                await title_el.get_attribute("title")
                            ).strip(),
                            "company": (await company_el.inner_text()).strip(),
                            "location": (await location_el.inner_text()).strip()
                            if location_el
                            else "",
                            "salary": (await salary_el.inner_text()).strip()
                            if salary_el
                            else "",
                            "source": "indeed",
                            "source_url": f"https://in.indeed.com{await title_el.get_attribute('href')}".split(
                                "?"
                            )[0]
                            if title_el
                            else "",
                            "description": "",
                        }
                    )

                await human_delay(2, 4)

        except Exception as e:
            print(f"Indeed scrape error: {e}")
        finally:
            await browser.close()

    asyncio.run(_scrape())
    return results
