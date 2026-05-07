from scraper.base import get_browser, human_delay
import asyncio
from typing import List, Dict, Optional


def scrape_linkedin(
    job_title: str, location: Optional[str], date_posted: str
) -> List[Dict]:
    """
    LinkedIn scraper - uses publicly available data only.
    Complies with DPDP Act 2023 by not scraping behind login gates.
    """
    results = []

    async def _scrape():
        browser, context = await get_browser()
        page = await context.new_page()

        try:
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}"
            if location:
                search_url += f"&location={location}"
            if date_posted == "past_24h":
                search_url += "&f_TPR=r86400"

            await page.goto(search_url, wait_until="networkidle")
            await human_delay(5, 8)

            job_cards = await page.query_selector_all(".base-search-card")

            for card in job_cards:
                title_el = await card.query_selector(".base-search-card__title")
                company_el = await card.query_selector(".base-search-card__subtitle")
                location_el = await card.query_selector(".job-search-card__location")
                link_el = await card.query_selector("a.base-card__full-link")

                if title_el and company_el:
                    results.append(
                        {
                            "job_title": (await title_el.inner_text()).strip(),
                            "company": (await company_el.inner_text()).strip(),
                            "location": (await location_el.inner_text()).strip()
                            if location_el
                            else "",
                            "source": "linkedin",
                            "source_url": (await link_el.get_attribute("href")).split(
                                "?"
                            )[0]
                            if link_el
                            else "",
                            "description": "",
                            "salary": "",
                        }
                    )

                await human_delay(2, 4)

        except Exception as e:
            print(f"LinkedIn scrape error: {e}")
        finally:
            await browser.close()

    asyncio.run(_scrape())
    return results
