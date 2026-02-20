"""
Web scraping base class and utilities
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from backend.config import settings


class BaseScraper(ABC):
    """Abstract base class for web scrapers"""
    
    def __init__(self, use_selenium: bool = False):
        self.use_selenium = use_selenium
        self.driver = None
        
        if use_selenium:
            self._init_selenium()
    
    def _init_selenium(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        
        if settings.SELENIUM_HEADLESS:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Warning: Could not initialize Chrome driver: {e}")
            self.driver = None
    
    def get_soup(self, url: str, use_selenium: bool = False) -> BeautifulSoup:
        """Get BeautifulSoup object from URL"""
        if use_selenium and self.driver:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            html = self.driver.page_source
        else:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            html = response.text
        
        return BeautifulSoup(html, 'lxml')
    
    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Get request headers"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    @abstractmethod
    def scrape(self, *args, **kwargs) -> Dict[str, Any]:
        """Abstract scrape method - must be implemented by subclasses"""
        pass
    
    def close(self):
        """Close Selenium driver"""
        if self.driver:
            self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class YahooFinanceScraper(BaseScraper):
    """Scraper for Yahoo Finance"""
    
    def scrape(self, ticker: str) -> Dict[str, Any]:
        """Scrape stock data from Yahoo Finance"""
        url = f"https://finance.yahoo.com/quote/{ticker}"
        
        try:
            soup = self.get_soup(url)
            
            # Extract price (example - actual selectors may vary)
            price_elem = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
            price = price_elem.text if price_elem else None
            
            # Extract other data
            data = {
                'ticker': ticker,
                'price': price,
                'source': 'Yahoo Finance',
                'url': url
            }
            
            return data
        
        except Exception as e:
            return {
                'ticker': ticker,
                'error': str(e),
                'source': 'Yahoo Finance'
            }


class NSEScraper(BaseScraper):
    """Scraper for NSE India"""
    
    def scrape(self, symbol: str) -> Dict[str, Any]:
        """Scrape stock data from NSE"""
        url = f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}"
        
        try:
            # NSE requires specific headers and cookies
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            
            session = requests.Session()
            session.get("https://www.nseindia.com", headers=headers)
            
            response = session.get(url, headers=headers)
            data = response.json() if response.status_code == 200 else {}
            
            return {
                'symbol': symbol,
                'data': data,
                'source': 'NSE India'
            }
        
        except Exception as e:
            return {
                'symbol': symbol,
                'error': str(e),
                'source': 'NSE India'
            }


class BSEScraper(BaseScraper):
    """Scraper for BSE India"""
    
    def scrape(self, scrip_code: str) -> Dict[str, Any]:
        """Scrape stock data from BSE"""
        url = f"https://www.bseindia.com/stock-share-price/stock-price.aspx?scripcode={scrip_code}"
        
        try:
            soup = self.get_soup(url)
            
            data = {
                'scrip_code': scrip_code,
                'source': 'BSE India',
                'url': url
            }
            
            return data
        
        except Exception as e:
            return {
                'scrip_code': scrip_code,
                'error': str(e),
                'source': 'BSE India'
            }
