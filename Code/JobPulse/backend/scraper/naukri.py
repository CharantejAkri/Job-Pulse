from scraper.base import get_browser, human_delay
import asyncio
from typing import List, Dict, Optional


def scrape_naukri(
    job_title: str, location: Optional[str], date_posted: str
) -> List[Dict]:
    """
    Naukri.com scraper - India's largest job board.
    Scrapes only publicly available job listings.
    """
    results = []

    async def _scrape():
        browser, context = await get_browser()
        page = await context.new_page()

        try:
            search_url = f"https://www.naukri.com/{job_title}-jobs"
            if location:
                search_url += f"-in-{location}"

            await page.goto(search_url, wait_until="networkidle")
            await human_delay(5, 8)

            job_cards = await page.query_selector_all(".srp-jobtuple-wrapper")

            for card in job_cards:
                title_el = await card.query_selector(".title")
                company_el = await card.query_selector(".comp-name")
                location_el = await card.query_selector(".loc")
                salary_el = await card.query_selector(".sal")
                desc_el = await card.query_selector(".job-description")

                if title_el and company_el:
                    results.append(
                        {
                            "job_title": (await title_el.get_attribute("title")).strip()
                            if title_el
                            else "",
                            "company": (await company_el.inner_text()).strip(),
                            "location": (await location_el.inner_text()).strip()
                            if location_el
                            else "",
                            "salary": (await salary_el.inner_text()).strip()
                            if salary_el
                            else "",
                            "source": "naukri",
                            "source_url": (await title_el.get_attribute("href")).split(
                                "?"
                            )[0]
                            if title_el
                            else "",
                            "description": (await desc_el.inner_text()).strip()
                            if desc_el
                            else "",
                        }
                    )

                await human_delay(2, 4)

        except Exception as e:
            print(f"Naukri scrape error: {e}")
        finally:
            await browser.close()

    asyncio.run(_scrape())
    return results
