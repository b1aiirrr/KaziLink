"""
MyJobMag.com Scraper
"""

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio
from typing import List, Dict
import re

class MyJobMagScraper:
    BASE_URL = "https://www.myjobmag.com"
    JOBS_URL = f"{BASE_URL}/jobs-by-country/kenya"
    
    async def scrape(self, max_pages: int = 5) -> List[Dict]:
        """Scrape jobs from MyJobMag"""
        jobs = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                for page_num in range(1, max_pages + 1):
                    url = f"{self.JOBS_URL}/page-{page_num}" if page_num > 1 else self.JOBS_URL
                    print(f"Scraping MyJobMag page {page_num}: {url}")
                    
                    await page.goto(url, wait_until='networkidle')
                    await asyncio.sleep(2)
                    
                    content = await page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Find job listings
                    job_cards = soup.find_all('div', class_=re.compile(r'job|listing|vacancy'))
                    
                    if not job_cards:
                        job_cards = soup.find_all('article') or soup.find_all('li', class_=re.compile(r'job'))
                    
                    print(f"Found {len(job_cards)} listings on page {page_num}")
                    
                    for card in job_cards:
                        try:
                            job_data = self._extract_job(card)
                            if job_data:
                                jobs.append(job_data)
                        except Exception as e:
                            print(f"Error: {e}")
                            continue
                
            finally:
                await browser.close()
        
        return jobs
    
    def _extract_job(self, card) -> Dict:
        """Extract job from card"""
        link = card.find('a', href=re.compile(r'/job/'))
        if not link:
            return None
        
        job_url = link.get('href')
        if not job_url.startswith('http'):
            job_url = f"{self.BASE_URL}{job_url}"
        
        title = (card.find('h2') or card.find('h3') or card.find(class_=re.compile(r'title'))).get_text(strip=True)
        company_elem = card.find(class_=re.compile(r'company|employer'))
        location_elem = card.find(class_=re.compile(r'location'))
        
        company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
        location = location_elem.get_text(strip=True) if location_elem else "Kenya"
        
        # Description might be in card or require visiting page
        desc_elem = card.find(class_=re.compile(r'description|summary'))
        description = desc_elem.get_text(strip=True) if desc_elem else title
        
        return {
            'title': title,
            'company': company,
            'location': location,
            'description': description,
            'source_url': job_url,
            'source_platform': 'myjobmag'
        }
