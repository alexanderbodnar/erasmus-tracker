import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DataStore:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from JSON file"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Error loading data file: {e}. Starting with empty data.")
                return {}
        return {}
    
    def save_data(self) -> None:
        """Save data to JSON file"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Data saved to {self.file_path}")
        except IOError as e:
            logger.error(f"Error saving data file: {e}")
    
    def get_last_check(self) -> Optional[str]:
        """Get timestamp of last check"""
        return self.data.get('last_check')
    
    def set_last_check(self, timestamp: str = None) -> None:
        """Set timestamp of last check"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        self.data['last_check'] = timestamp
        self.save_data()
    
    def get_known_posts(self) -> List[Dict]:
        """Get list of known posts"""
        return self.data.get('known_posts', [])
    
    def add_post(self, post: Dict) -> None:
        """Add a new post to known posts"""
        if 'known_posts' not in self.data:
            self.data['known_posts'] = []
        
        # Check if post already exists (by URL or title)
        for existing_post in self.data['known_posts']:
            if (existing_post.get('url') == post.get('url') or 
                existing_post.get('title') == post.get('title')):
                return  # Post already exists
        
        self.data['known_posts'].append(post)
        self.save_data()
        logger.info(f"Added new post: {post.get('title', 'Unknown title')}")
    
    def is_new_post(self, post: Dict) -> bool:
        """Check if a post is new (not in known posts)"""
        known_posts = self.get_known_posts()
        
        for existing_post in known_posts:
            if (existing_post.get('url') == post.get('url') or 
                existing_post.get('title') == post.get('title')):
                return False
        
        return True
    
    def get_stats(self) -> Dict:
        """Get statistics about stored data"""
        return {
            'total_posts': len(self.get_known_posts()),
            'last_check': self.get_last_check(),
            'data_file': self.file_path
        }