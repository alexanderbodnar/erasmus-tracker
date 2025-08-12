#!/usr/bin/env python3
"""
Demo script to test scraping functionality without email configuration
"""

import sys
import logging
import os
from scraper import ErasmusScraper
from data_store import DataStore

def setup_logging():
    """Setup basic logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def test_scraping():
    """Test the scraping functionality"""
    logger = logging.getLogger(__name__)
    
    print("🕷️ Testing Erasmus Scraper...")
    print("=" * 50)
    
    try:
        # Create scraper
        scraper = ErasmusScraper()
        
        # Try to scrape posts
        print(f"📡 Fetching posts from: https://erasmus.tuke.sk/vyzvy-na-studentsku-mobilitu/")
        posts = scraper.scrape_posts()
        
        print(f"✅ Found {len(posts)} posts")
        
        if posts:
            print("\n📋 Posts found:")
            for i, post in enumerate(posts[:5], 1):  # Show first 5 posts
                title = post.get('title', 'No title')[:60]
                date = post.get('date', 'No date')
                url = post.get('url', 'No URL')
                print(f"  {i}. {title}...")
                print(f"     Date: {date}")
                print(f"     URL: {url}")
                print()
        else:
            print("⚠️  No posts found. This could be due to:")
            print("   - Website structure changes")
            print("   - Network connectivity issues")
            print("   - Website blocking automated requests")
        
        # Test data storage
        print("💾 Testing data storage...")
        data_store = DataStore('test_data.json')
        
        for post in posts[:3]:  # Store first 3 posts as test
            if data_store.is_new_post(post):
                data_store.add_post(post)
                print(f"   ✅ Stored: {post.get('title', 'No title')[:40]}...")
        
        stats = data_store.get_stats()
        print(f"   📊 Total stored posts: {stats['total_posts']}")
        
        # Cleanup test file
        if os.path.exists('test_data.json'):
            os.remove('test_data.json')
            print("   🧹 Cleaned up test data file")
        
        print("\n🎉 Scraping test completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during scraping test: {e}")
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def main():
    setup_logging()
    
    print("🎓 Erasmus Tracker - Scraping Demo")
    print("This demo tests the scraping functionality without requiring email setup.\n")
    
    success = test_scraping()
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("\nNext steps:")
        print("1. Configure your email settings in .env file")
        print("2. Run 'python main.py --test-email' to test email")
        print("3. Run 'python main.py' to start monitoring")
    else:
        print("\n❌ Demo failed. Check the logs for details.")
        sys.exit(1)

if __name__ == '__main__':
    main()