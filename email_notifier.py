import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import logging
from config import Config

logger = logging.getLogger(__name__)

class EmailNotifier:
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.email_from = Config.EMAIL_FROM
        self.email_password = Config.EMAIL_PASSWORD
        self.email_to = Config.EMAIL_TO
    
    def create_email_content(self, posts: List[Dict]) -> tuple[str, str]:
        """Create email subject and body content"""
        if len(posts) == 1:
            subject = f"New Erasmus Post: {posts[0].get('title', 'Unknown Title')}"
        else:
            subject = f"New Erasmus Posts: {len(posts)} new posts found"
        
        # Create HTML content
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f8ff; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .post {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }}
                .post-title {{ color: #1e90ff; font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
                .post-date {{ color: #666; font-size: 14px; margin-bottom: 10px; }}
                .post-content {{ margin-bottom: 10px; }}
                .post-url {{ margin-top: 10px; }}
                .post-url a {{ color: #1e90ff; text-decoration: none; }}
                .post-url a:hover {{ text-decoration: underline; }}
                .footer {{ margin-top: 30px; padding: 15px; background-color: #f9f9f9; border-radius: 5px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🎓 New Erasmus Posts Detected!</h2>
                <p>Found {len(posts)} new post(s) on the Erasmus TUKE website.</p>
            </div>
        """
        
        for post in posts:
            title = post.get('title', 'Unknown Title')
            date = post.get('date', 'Unknown Date')
            content = post.get('content', 'No content available')
            url = post.get('url', '#')
            
            html_body += f"""
            <div class="post">
                <div class="post-title">{title}</div>
                <div class="post-date">📅 Date: {date}</div>
                <div class="post-content">{content}</div>
                <div class="post-url">
                    <a href="{url}" target="_blank">🔗 View Full Post</a>
                </div>
            </div>
            """
        
        html_body += f"""
            <div class="footer">
                <p>This email was sent by the Erasmus Tracker system.</p>
                <p>Website: <a href="{Config.TARGET_URL}">{Config.TARGET_URL}</a></p>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_body = f"New Erasmus Posts Detected!\n\n"
        text_body += f"Found {len(posts)} new post(s) on the Erasmus TUKE website.\n\n"
        
        for i, post in enumerate(posts, 1):
            title = post.get('title', 'Unknown Title')
            date = post.get('date', 'Unknown Date')
            content = post.get('content', 'No content available')
            url = post.get('url', '#')
            
            text_body += f"Post #{i}:\n"
            text_body += f"Title: {title}\n"
            text_body += f"Date: {date}\n"
            text_body += f"Content: {content}\n"
            text_body += f"URL: {url}\n\n"
        
        text_body += f"Website: {Config.TARGET_URL}\n"
        
        return subject, html_body, text_body
    
    def send_notification(self, posts: List[Dict]) -> bool:
        """Send email notification for new posts"""
        if not posts:
            logger.info("No posts to notify about")
            return True
        
        try:
            # Create email content
            subject, html_body, text_body = self.create_email_content(posts)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            
            # Create text and HTML parts
            text_part = MIMEText(text_body, 'plain', 'utf-8')
            html_part = MIMEText(html_body, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_from, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent successfully to {self.email_to}")
            logger.info(f"Subject: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    def send_test_email(self) -> bool:
        """Send a test email to verify configuration"""
        try:
            subject = "Erasmus Tracker - Test Email"
            body = """
            <html>
            <body>
                <h2>🧪 Test Email</h2>
                <p>This is a test email from your Erasmus Tracker system.</p>
                <p>If you receive this email, your email configuration is working correctly!</p>
                <p>The system is now ready to notify you about new Erasmus posts.</p>
            </body>
            </html>
            """
            
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_from, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Test email sent successfully to {self.email_to}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send test email: {e}")
            return False