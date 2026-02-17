"""
Fuzu.com Scraper
Scrapes job listings from Fuzu job board
"""

from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup
import asyncio
from typing import List, Dict
import re

class FuzuScraper:
    BASE_URL = "https://www.fuzu.com"
    JOBS_URL = f"{BASE_URL}/ke/jobs"
    
    def __init__(self):
        self.jobs = []
    
    async def scrape(self, max_pages: int = 5) -> List[Dict]:
        """Scrape jobs from Fuzu"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                for page_num in range(1, max_pages + 1):
                    url = f"{self.JOBS_URL}?page={page_num}"
                    print(f"Scraping Fuzu page {page_num}: {url}")
                    
                    await page.goto(url, wait_until='networkidle')
                    await asyncio.sleep(2)  # Be respectful
                    
                    # Get page content
                    content = await page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Find job cards (adjust selectors based on actual site structure)
                    job_cards = soup.find_all('div', class_=re.compile(r'job-card|job-item|listing'))
                    
                    if not job_cards:
                        # Try alternative selectors
                        job_cards = soup.find_all('article') or soup.find_all('a', href=re.compile(r'/jobs/'))
                    
                    print(f"Found {len(job_cards)} job listings on page {page_num}")
                    
                    for card in job_cards:
                        try:
                            job_data = await self._extract_job_data(card, page)
                            if job_data:
                                self.jobs.append(job_data)
                        except Exception as e:
                            print(f"Error extracting job: {e}")
                            continue
                    
                    # Check if there's a next page
                    next_button = soup.find('a', text=re.compile(r'Next|›|»'))
                    if not next_button:
                        break
                
            finally:
                await browser.close()
        
        return self.jobs
    
    async def _extract_job_data(self, card, page: Page) -> Dict:
        """Extract job details from card"""
        # Find job link
        link_elem = card.find('a', href=re.compile(r'/jobs/'))
        if not link_elem:
            return None
        
        job_url = link_elem.get('href')
        if not job_url.startswith('http'):
            job_url = f"{self.BASE_URL}{job_url}"
        
        # Extract basic info from card
        title_elem = card.find('h2') or card.find('h3') or card.find(class_=re.compile(r'title|heading'))
        company_elem = card.find(class_=re.compile(r'company|employer'))
        location_elem = card.find(class_=re.compile(r'location|city'))
        
        title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
        company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
        location = location_elem.get_text(strip=True) if location_elem else "Kenya"
        
        # Get full description by visiting the job page
        description = await self._get_full_description(page, job_url)
        
        return {
            'title': title,
            'company': company,
            'location': location,
            'description': description,
            'source_url': job_url,
            'source_platform': 'fuzu'
        }
    
    async def _get_full_description(self, page: Page, url: str) -> str:
        """Visit job page to get full description"""
        try:
            await page.goto(url, timeout=10000)
            await asyncio.sleep(1)
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find description container
            desc_elem = (
                soup.find('div', class_=re.compile(r'description|details|content')) or
                soup.find('div', id=re.compile(r'description|details'))
            )
            
            if desc_elem:
                return desc_elem.get_text(strip=True, separator=' ')
            
            return "Description not available"
            
        except Exception as e:
            print(f"Error getting description from {url}: {e}")
            return "Description not available"


# Test the scraper
if __name__ == "__main__":
    async def test():
        scraper = FuzuScraper()
        jobs = await scraper.scrape(max_pages=2)
        print(f"\nScraped {len(jobs)} jobs from Fuzu")
        
        if jobs:
            print(f"\nSample job:")
            print(f"Title: {jobs[0]['title']}")
            print(f"Company: {jobs[0]['company']}")
            print(f"Location: {jobs[0]['location']}")
    
    asyncio.run(test())
