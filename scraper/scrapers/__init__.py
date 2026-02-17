"""
Scrapers package initialization
"""

from .fuzu import FuzuScraper
from .myjobmag import MyJobMagScraper
from .brightermonday import BrighterMondayScraper

__all__ = ['FuzuScraper', 'MyJobMagScraper', 'BrighterMondayScraper']
