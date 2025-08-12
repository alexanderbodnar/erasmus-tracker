# Erasmus Tracker 🎓

A Python web scraper that monitors the [TUKE Erasmus website](https://erasmus.tuke.sk/vyzvy-na-studentsku-mobilitu/) for new student mobility posts and sends email notifications when new opportunities are available.

## Features

- 🕷️ **Web Scraping**: Automatically scrapes the TUKE Erasmus website for new posts
- 📧 **Email Notifications**: Sends formatted HTML email alerts when new posts are detected
- 💾 **Data Persistence**: Tracks previously seen posts to avoid duplicate notifications
- ⚙️ **Configurable**: Easy configuration via environment variables
- 📊 **Statistics**: View stats about tracked posts and system status
- 🧪 **Testing**: Built-in email configuration testing

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alexanderbodnar/erasmus-tracker.git
   cd erasmus-tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your email configuration
   ```

## Configuration

Edit the `.env` file with your settings:

```env
# Email Configuration (Required)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_TO=recipient@gmail.com

# Scraping Configuration (Optional)
TARGET_URL=https://erasmus.tuke.sk/vyzvy-na-studentsku-mobilitu/
CHECK_INTERVAL_HOURS=6
LAST_KNOWN_DATE=2024-05-06

# Logging (Optional)
LOG_LEVEL=INFO
```

### Email Setup

For **Gmail** users:
1. Enable 2-factor authentication
2. Generate an [App Password](https://support.google.com/accounts/answer/185833)
3. Use the app password in `EMAIL_PASSWORD`

For **other email providers**, adjust `SMTP_SERVER` and `SMTP_PORT` accordingly.

## Usage

### Run a Single Check
```bash
python main.py
```

### Test Email Configuration
```bash
python main.py --test-email
```

### View Statistics
```bash
python main.py --stats
```

### Set Log Level
```bash
python main.py --log-level DEBUG
```

## Scheduling

To run the scraper automatically, set up a cron job:

```bash
# Edit crontab
crontab -e

# Add line to check every 6 hours
0 */6 * * * cd /path/to/erasmus-tracker && python main.py
```

## How It Works

1. **Scraping**: The scraper fetches the TUKE Erasmus webpage and parses it for post content
2. **Date Filtering**: Only posts newer than the configured `LAST_KNOWN_DATE` are considered
3. **Duplicate Detection**: Previously seen posts are stored in `erasmus_data.json` to avoid duplicates
4. **Email Notification**: New posts trigger formatted HTML email notifications
5. **Logging**: All activities are logged to both console and `erasmus_tracker.log`

## Project Structure

```
erasmus-tracker/
├── main.py              # Main entry point and CLI
├── config.py            # Configuration management
├── scraper.py           # Web scraping logic
├── email_notifier.py    # Email notification system
├── data_store.py        # Data persistence layer
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Data Storage

The application stores data in `erasmus_data.json`:
- `last_check`: Timestamp of last scraping attempt
- `known_posts`: Array of previously seen posts with titles, URLs, dates, and content

## Email Format

Notifications include:
- 📧 **Subject**: "New Erasmus Post" or "New Erasmus Posts: X new posts found"
- 🎨 **HTML Content**: Formatted email with post titles, dates, descriptions, and links
- 📱 **Plain Text**: Fallback text version for all email clients

## Logging

Logs are written to:
- **Console**: Real-time output
- **File**: `erasmus_tracker.log` for persistence

Log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`

## Error Handling

The application handles:
- 🌐 Network connectivity issues
- 📧 Email sending failures
- 📄 Webpage parsing errors
- 💾 Data file corruption
- ⚙️ Configuration validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter issues:
1. Check the logs in `erasmus_tracker.log`
2. Verify your email configuration with `--test-email`
3. Review your `.env` file settings
4. Open an issue on GitHub

---

🎓 **Happy Erasmus hunting!** This tool helps you stay updated on new student mobility opportunities at TUKE.