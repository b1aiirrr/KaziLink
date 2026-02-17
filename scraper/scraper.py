"""
Main scraper orchestrator for KaziLink
Coordinates scraping from all sources, categorizes, and saves to Supabase
"""

import asyncio
import os
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
from supabase import create_client, Client

from scrapers.fuzu import FuzuScraper
from scrapers.myjobmag import MyJobMagScraper
from scrapers.brightermonday import BrighterMondayScraper
from categorizer import OpportunityCategorizer

load_dotenv()

class KaziLinkScraper:
    def __init__(self):
        # Initialize Supabase
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        self.supabase: Client = create_client(supabase_url, supabase_key)
        
        # Initialize categorizer
        self.categorizer = OpportunityCategorizer()
        
        # Initialize site scrapers
        self.scrapers = {
            'fuzu': FuzuScraper(),
            'myjobmag': MyJobMagScraper(),
            'brightermonday': BrighterMondayScraper()
        }
    
    async def scrape_all(self, max_pages_per_site: int = 3) -> Dict[str, List[Dict]]:
        """Scrape all job boards concurrently"""
        print("🚀 Starting KaziLink scraper...")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Run scrapers in parallel
        tasks = []
        for name, scraper in self.scrapers.items():
            print(f"📊 Launching {name} scraper...")
            tasks.append(scraper.scrape(max_pages=max_pages_per_site))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Organize results
        all_jobs = {}
        for i, name in enumerate(self.scrapers.keys()):
            if isinstance(results[i], Exception):
                print(f"❌ {name} failed: {results[i]}")
                all_jobs[name] = []
            else:
                all_jobs[name] = results[i]
                print(f"✅ {name}: {len(results[i])} jobs")
        
        return all_jobs
    
    def categorize_jobs(self, all_jobs: Dict[str, List[Dict]]) -> List[Dict]:
        """Categorize all scraped jobs using LLM"""
        print("\n🤖 Categorizing opportunities with GPT-4...")
        
        # Flatten jobs from all sources
        flat_jobs = []
        for source, jobs in all_jobs.items():
            flat_jobs.extend(jobs)
        
        # Remove duplicates by URL
        unique_jobs = {job['source_url']: job for job in flat_jobs}.values()
        unique_jobs = list(unique_jobs)
        
        print(f"📦 Found {len(unique_jobs)} unique opportunities")
        
        # Categorize
        categorized = self.categorizer.batch_categorize(unique_jobs)
        
        # Count by type
        counts = {'attachment': 0, 'internship': 0, 'job': 0}
        for job in categorized:
            counts[job['type']] += 1
        
        print(f"📎 Attachments: {counts['attachment']}")
        print(f"🎓 Internships: {counts['internship']}")
        print(f"💼 Jobs: {counts['job']}")
        
        return categorized
    
    def save_to_supabase(self, jobs: List[Dict], dry_run: bool = False):
        """Save categorized jobs to Supabase"""
        if dry_run:
            print("\n🔍 DRY RUN - Not saving to database")
            return
        
        print("\n💾 Saving to Supabase...")
        
        saved = 0
        skipped = 0
        errors = 0
        
        for job in jobs:
            try:
                # Check if job already exists
                existing = self.supabase.table('opportunities')\
                    .select('id')\
                    .eq('source_url', job['source_url'])\
                    .execute()
                
                if existing.data:
                    print(f"⏭️  Skipping duplicate: {job['title']}")
                    skipped += 1
                    continue
                
                # Insert new opportunity
                data = {
                    'title': job['title'],
                    'company': job['company'],
                    'type': job['type'],
                    'description': job['description'],
                    'location': job['location'],
                    'source_url': job['source_url'],
                    'source_platform': job['source_platform'],
                    'status': 'active'
                }
                
                self.supabase.table('opportunities').insert(data).execute()
                print(f"✅ Saved: {job['title']} ({job['type']})")
                saved += 1
                
            except Exception as e:
                print(f"❌ Error saving {job['title']}: {e}")
                errors += 1
        
        print(f"\n📊 Summary:")
        print(f"   ✅ Saved: {saved}")
        print(f"   ⏭️  Skipped: {skipped}")
        print(f"   ❌ Errors: {errors}")
    
    async def run(self, dry_run: bool = False, max_pages: int = 3):
        """Main execution flow"""
        start_time = datetime.now()
        
        # Step 1: Scrape
        all_jobs = await self.scrape_all(max_pages_per_site=max_pages)
        
        # Step 2: Categorize
        categorized_jobs = self.categorize_jobs(all_jobs)
        
        # Step 3: Save
        self.save_to_supabase(categorized_jobs, dry_run=dry_run)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n⏱️  Total time: {elapsed:.2f} seconds")
        print("🎉 Scraping complete!")


# Entry point
async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='KaziLink Opportunity Scraper')
    parser.add_argument('--dry-run', action='store_true', help='Run without saving to database')
    parser.add_argument('--pages', type=int, default=3, help='Max pages per site (default: 3)')
    
    args = parser.parse_args()
    
    scraper = KaziLinkScraper()
    await scraper.run(dry_run=args.dry_run, max_pages=args.pages)


if __name__ == "__main__":
    asyncio.run(main())
