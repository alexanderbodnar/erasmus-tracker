import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class Config:
    # Email settings
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_FROM = os.getenv('EMAIL_FROM')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_TO = os.getenv('EMAIL_TO')
    
    # Scraping settings
    TARGET_URL = os.getenv('TARGET_URL', 'https://erasmus.tuke.sk/vyzvy-na-studentsku-mobilitu/')
    CHECK_INTERVAL_HOURS = int(os.getenv('CHECK_INTERVAL_HOURS', '6'))
    LAST_KNOWN_DATE = os.getenv('LAST_KNOWN_DATE', '2024-05-06')
    
    # Application settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    DATA_FILE = 'erasmus_data.json'
    
    # User agent for web scraping
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_fields = ['EMAIL_FROM', 'EMAIL_PASSWORD', 'EMAIL_TO']
        missing = [field for field in required_fields if not getattr(cls, field)]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True