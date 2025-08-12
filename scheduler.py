#!/usr/bin/env python3
"""
Scheduler script for running Erasmus Tracker periodically
"""

import time
import logging
import sys
from datetime import datetime, timedelta
import subprocess
import argparse

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('scheduler.log')
        ]
    )

def run_tracker():
    """Run the main tracker script"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Running Erasmus Tracker...")
        result = subprocess.run([sys.executable, 'main.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logger.info("Tracker completed successfully")
            logger.debug(f"Output: {result.stdout}")
        else:
            logger.error(f"Tracker failed with exit code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        logger.error("Tracker timed out after 5 minutes")
        return False
    except Exception as e:
        logger.error(f"Error running tracker: {e}")
        return False

def scheduler_loop(interval_hours: int):
    """Main scheduler loop"""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting scheduler with {interval_hours} hour intervals")
    
    next_run = datetime.now()
    
    while True:
        current_time = datetime.now()
        
        if current_time >= next_run:
            logger.info(f"Starting scheduled run at {current_time}")
            
            success = run_tracker()
            
            if success:
                logger.info("Scheduled run completed successfully")
            else:
                logger.warning("Scheduled run failed")
            
            # Calculate next run time
            next_run = current_time + timedelta(hours=interval_hours)
            logger.info(f"Next run scheduled for: {next_run}")
        
        # Sleep for 1 minute before checking again
        time.sleep(60)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Erasmus Tracker Scheduler')
    parser.add_argument('--interval', type=int, default=6, 
                       help='Check interval in hours (default: 6)')
    parser.add_argument('--run-once', action='store_true',
                       help='Run once and exit (for testing)')
    
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    if args.run_once:
        logger.info("Running tracker once...")
        success = run_tracker()
        sys.exit(0 if success else 1)
    
    try:
        scheduler_loop(args.interval)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()