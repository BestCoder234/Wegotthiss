#!/bin/bash

# Daily Market Data Update Script
# This script fetches fresh market data every day

echo "🔄 Starting daily market data update at $(date)"

# Change to project directory
cd "$(dirname "$0")"

# Activate Python environment (if using virtual environment)
# source .venv/bin/activate  # Uncomment if using virtual environment

# Run the market data fetch script
python api/fetch_real_market_data.py

echo "✅ Daily update completed at $(date)" 