"""
BrighterMonday.co.ke Scraper
"""

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio
from typing import List, Dict
import re

class BrighterMondayScraper:
    BASE_URL = "https://www.brightermonday.co.ke"
    JOBS_URL = f"{BASE_URL}/jobs"
    
    async def scrape(self, max_pages: int = 5) -> List[Dict]:
        """Scrape jobs from BrighterMonday"""
        jobs = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                for page_num in range(1, max_pages + 1):
                    url = f"{self.JOBS_URL}?page={page_num}"
                    print(f"Scraping BrighterMonday page {page_num}: {url}")
                    
                    await page.goto(url, wait_until='networkidle')
                    await asyncio.sleep(2)
                    
                    content = await page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Find job cards
                    job_cards = soup.find_all(['div', 'article'], class_=re.compile(r'job|search-result'))
                    
                    print(f"Found {len(job_cards)} listings")
                    
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
        """Extract job details"""
        link = card.find('a', href=re.compile(r'/job-vacancies/'))
        if not link:
            return None
        
        job_url = link.get('href')
        if not job_url.startswith('http'):
            job_url = f"{self.BASE_URL}{job_url}"
        
        title_elem = card.find(['h2', 'h3'], class_=re.compile(r'title|heading'))
        company_elem = card.find(class_=re.compile(r'company|organization'))
        location_elem = card.find(class_=re.compile(r'location|region'))
        
        title = title_elem.get_text(strip=True) if title_elem else link.get_text(strip=True)
        company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
        location = location_elem.get_text(strip=True) if location_elem else "Kenya"
        
        desc_elem = card.find(class_=re.compile(r'description|snippet|summary'))
        description = desc_elem.get_text(strip=True) if desc_elem else title
        
        return {
            'title': title,
            'company': company,
            'location': location,
            'description': description,
            'source_url': job_url,
            'source_platform': 'brightermonday'
        }
