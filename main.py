#!/usr/bin/env python3
"""
Erasmus Tracker - Web scraper for monitoring new Erasmus posts
"""

import logging
import sys
import argparse
from datetime import datetime
from typing import List, Dict

from config import Config
from scraper import ErasmusScraper
from email_notifier import EmailNotifier
from data_store import DataStore

def setup_logging(level: str = 'INFO'):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('erasmus_tracker.log')
        ]
    )

def check_for_new_posts() -> List[Dict]:
    """Check for new posts and return them"""
    logger = logging.getLogger(__name__)
    
    # Initialize components
    scraper = ErasmusScraper()
    data_store = DataStore(Config.DATA_FILE)
    
    logger.info("Starting post check...")
    
    # Scrape current posts
    current_posts = scraper.scrape_posts()
    
    if not current_posts:
        logger.warning("No posts found during scraping")
        return []
    
    # Filter for new posts
    new_posts = []
    for post in current_posts:
        if data_store.is_new_post(post):
            new_posts.append(post)
            data_store.add_post(post)
    
    # Update last check time
    data_store.set_last_check()
    
    logger.info(f"Found {len(new_posts)} new posts out of {len(current_posts)} total posts")
    
    return new_posts

def send_notifications(posts: List[Dict]) -> bool:
    """Send email notifications for new posts"""
    logger = logging.getLogger(__name__)
    
    if not posts:
        logger.info("No new posts to notify about")
        return True
    
    notifier = EmailNotifier()
    success = notifier.send_notification(posts)
    
    if success:
        logger.info(f"Successfully sent notification for {len(posts)} new posts")
    else:
        logger.error("Failed to send email notification")
    
    return success

def run_check():
    """Main function to run a single check"""
    logger = logging.getLogger(__name__)
    
    try:
        # Validate configuration
        Config.validate()
        
        # Check for new posts
        new_posts = check_for_new_posts()
        
        # Send notifications if there are new posts
        if new_posts:
            send_notifications(new_posts)
            
            # Log new posts
            logger.info("New posts found:")
            for post in new_posts:
                logger.info(f"  - {post.get('title', 'Unknown title')} ({post.get('date', 'Unknown date')})")
        else:
            logger.info("No new posts found")
        
        return len(new_posts)
        
    except Exception as e:
        logger.error(f"Error during check: {e}")
        return -1

def test_email():
    """Test email configuration"""
    logger = logging.getLogger(__name__)
    
    try:
        Config.validate()
        notifier = EmailNotifier()
        success = notifier.send_test_email()
        
        if success:
            logger.info("Test email sent successfully!")
            return True
        else:
            logger.error("Failed to send test email")
            return False
            
    except Exception as e:
        logger.error(f"Error testing email: {e}")
        return False

def show_stats():
    """Show statistics about stored data"""
    logger = logging.getLogger(__name__)
    
    data_store = DataStore(Config.DATA_FILE)
    stats = data_store.get_stats()
    
    print("\n📊 Erasmus Tracker Statistics")
    print("=" * 40)
    print(f"Total known posts: {stats['total_posts']}")
    print(f"Last check: {stats['last_check'] or 'Never'}")
    print(f"Data file: {stats['data_file']}")
    print(f"Target URL: {Config.TARGET_URL}")
    print(f"Email recipient: {Config.EMAIL_TO}")
    
    # Show recent posts
    recent_posts = data_store.get_known_posts()[-5:]  # Last 5 posts
    if recent_posts:
        print(f"\n🆕 Recent posts (last {len(recent_posts)}):")
        for i, post in enumerate(reversed(recent_posts), 1):
            title = post.get('title', 'Unknown title')[:50]
            date = post.get('date', 'Unknown date')
            print(f"  {i}. {title}... ({date})")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Erasmus Tracker - Monitor new Erasmus posts')
    parser.add_argument('--test-email', action='store_true', help='Send a test email')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Set logging level')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Erasmus Tracker")
    
    if args.test_email:
        success = test_email()
        sys.exit(0 if success else 1)
    
    if args.stats:
        show_stats()
        sys.exit(0)
    
    # Run the main check
    result = run_check()
    
    if result == -1:
        logger.error("Check failed")
        sys.exit(1)
    else:
        logger.info(f"Check completed successfully. Found {result} new posts.")
        sys.exit(0)

if __name__ == '__main__':
    main()