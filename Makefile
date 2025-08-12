# Erasmus Tracker Makefile

.PHONY: help install test demo stats clean setup

# Default target
help:
	@echo "Erasmus Tracker - Available commands:"
	@echo ""
	@echo "  make setup       - Initial setup (install deps, copy config)"
	@echo "  make install     - Install Python dependencies"
	@echo "  make demo        - Run scraping demo (no email required)"
	@echo "  make test        - Test email configuration"
	@echo "  make run         - Run single check"
	@echo "  make stats       - Show statistics"
	@echo "  make schedule    - Run scheduler (continuous mode)"
	@echo "  make clean       - Clean up log files and data"
	@echo ""

# Initial setup
setup: install
	@echo "Setting up Erasmus Tracker..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file from template"; \
		echo "⚠️  Please edit .env with your email configuration"; \
	else \
		echo "✅ .env file already exists"; \
	fi

# Install dependencies
install:
	@echo "Installing Python dependencies..."
	pip install --user -r requirements.txt
	@echo "✅ Dependencies installed"

# Run demo
demo:
	@echo "Running scraping demo..."
	python demo.py

# Test email
test:
	@echo "Testing email configuration..."
	python main.py --test-email

# Run single check
run:
	@echo "Running Erasmus Tracker..."
	python main.py

# Show statistics
stats:
	@echo "Showing statistics..."
	python main.py --stats

# Run scheduler
schedule:
	@echo "Starting scheduler..."
	python scheduler.py

# Clean up
clean:
	@echo "Cleaning up..."
	rm -f *.log
	rm -f erasmus_data.json
	rm -f test_data.json
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Development targets
lint:
	@echo "Running linter..."
	python -m py_compile *.py
	@echo "✅ Syntax check complete"

# Check configuration
check-config:
	@echo "Checking configuration..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@echo "✅ Configuration file exists"