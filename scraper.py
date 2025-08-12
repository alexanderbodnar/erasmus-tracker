import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import re
from config import Config

logger = logging.getLogger(__name__)

class ErasmusScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': Config.USER_AGENT
        })
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch webpage content"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching page {url}: {e}")
            return None
    
    def parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse date string from the website"""
        if not date_string:
            return None
        
        # Common Slovak date patterns
        patterns = [
            r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})',  # d.m.yyyy or dd.mm.yyyy
            r'(\d{1,2})\s+(\w+)\s+(\d{4})',          # d month yyyy
            r'(\d{4})-(\d{2})-(\d{2})',              # yyyy-mm-dd
        ]
        
        # Slovak month names mapping
        slovak_months = {
            'január': 1, 'február': 2, 'marec': 3, 'apríl': 4,
            'máj': 5, 'jún': 6, 'júl': 7, 'august': 8,
            'september': 9, 'október': 10, 'november': 11, 'december': 12
        }
        
        for pattern in patterns:
            match = re.search(pattern, date_string.lower())
            if match:
                try:
                    if pattern == patterns[0]:  # d.m.yyyy
                        day, month, year = match.groups()
                        return datetime(int(year), int(month), int(day))
                    elif pattern == patterns[1]:  # d month yyyy
                        day, month_name, year = match.groups()
                        month = slovak_months.get(month_name, None)
                        if month:
                            return datetime(int(year), month, int(day))
                    elif pattern == patterns[2]:  # yyyy-mm-dd
                        year, month, day = match.groups()
                        return datetime(int(year), int(month), int(day))
                except ValueError:
                    continue
        
        logger.warning(f"Could not parse date: {date_string}")
        return None
    
    def extract_posts(self, html: str) -> List[Dict]:
        """Extract posts from HTML content"""
        soup = BeautifulSoup(html, 'lxml')
        posts = []
        
        # Look for common post patterns on Slovak university websites
        # This is a generic approach since we can't access the actual site
        post_selectors = [
            '.post', '.article', '.news-item', '.content-item',
            '[class*="post"]', '[class*="article"]', '[class*="news"]',
            'article', '.entry', '.item'
        ]
        
        for selector in post_selectors:
            post_elements = soup.select(selector)
            if post_elements:
                logger.info(f"Found {len(post_elements)} posts with selector: {selector}")
                
                for element in post_elements:
                    post = self._extract_post_data(element)
                    if post:
                        posts.append(post)
                break  # Use first successful selector
        
        # If no posts found with common selectors, try to find any content with dates
        if not posts:
            posts = self._extract_posts_fallback(soup)
        
        return posts
    
    def _extract_post_data(self, element) -> Optional[Dict]:
        """Extract individual post data from element"""
        try:
            # Extract title
            title_selectors = ['h1', 'h2', 'h3', 'h4', '.title', '[class*="title"]', 'a']
            title = None
            title_element = None
            
            for selector in title_selectors:
                title_element = element.select_one(selector)
                if title_element:
                    title = title_element.get_text(strip=True)
                    if title:
                        break
            
            if not title:
                return None
            
            # Extract URL
            url = None
            if title_element and title_element.name == 'a':
                url = title_element.get('href')
            else:
                link = element.select_one('a[href]')
                if link:
                    url = link.get('href')
            
            # Make URL absolute if relative
            if url and url.startswith('/'):
                url = f"https://erasmus.tuke.sk{url}"
            
            # Extract date
            date_text = element.get_text()
            post_date = self.parse_date(date_text)
            
            # Extract content/description
            content = element.get_text(strip=True)
            if len(content) > 300:
                content = content[:300] + "..."
            
            post = {
                'title': title,
                'url': url,
                'date': post_date.isoformat() if post_date else None,
                'content': content,
                'scraped_at': datetime.now().isoformat()
            }
            
            return post
            
        except Exception as e:
            logger.warning(f"Error extracting post data: {e}")
            return None
    
    def _extract_posts_fallback(self, soup: BeautifulSoup) -> List[Dict]:
        """Fallback method to extract posts when standard selectors fail"""
        posts = []
        
        # Look for any text containing date patterns
        text_elements = soup.find_all(text=True)
        
        for text in text_elements:
            if self.parse_date(text):
                parent = text.parent
                if parent:
                    post = self._extract_post_data(parent)
                    if post:
                        posts.append(post)
        
        return posts
    
    def scrape_posts(self) -> List[Dict]:
        """Main scraping method"""
        logger.info(f"Scraping posts from {Config.TARGET_URL}")
        
        html = self.fetch_page(Config.TARGET_URL)
        if not html:
            return []
        
        posts = self.extract_posts(html)
        
        # Filter posts newer than the last known date
        cutoff_date = datetime.strptime(Config.LAST_KNOWN_DATE, '%Y-%m-%d')
        recent_posts = []
        
        for post in posts:
            if post.get('date'):
                post_date = datetime.fromisoformat(post['date'])
                if post_date > cutoff_date:
                    recent_posts.append(post)
            else:
                # If no date found, include the post to be safe
                recent_posts.append(post)
        
        logger.info(f"Found {len(recent_posts)} posts newer than {Config.LAST_KNOWN_DATE}")
        return recent_posts