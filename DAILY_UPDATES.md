# Daily Market Data Updates

## Current Status
✅ **Real market data** is being fetched from Yahoo Finance API
❌ **Automatic daily updates** are NOT currently running

## How to Set Up Automatic Daily Updates

### Option 1: Using Cron (Recommended)

1. **Open your crontab:**
   ```bash
   crontab -e
   ```

2. **Add this line to run updates daily at 6:00 PM IST:**
   ```bash
   0 18 * * * /Users/kushdatta/Desktop/This\ time\ frrr/run_daily_updates.sh >> /tmp/market_updates.log 2>&1
   ```

3. **Or run at 9:00 AM IST (after market opens):**
   ```bash
   0 9 * * * /Users/kushdatta/Desktop/This\ time\ frrr/run_daily_updates.sh >> /tmp/market_updates.log 2>&1
   ```

### Option 2: Using Python Scheduler

1. **Run the scheduler script:**
   ```bash
   python api/schedule_daily_update.py
   ```

2. **This will:**
   - Update data immediately
   - Schedule daily updates at 6:00 PM IST
   - Keep running in the background

### Option 3: Manual Updates

Run this command whenever you want fresh data:
```bash
python api/fetch_real_market_data.py
```

## What Gets Updated

- **Stock Prices**: Real closing prices from Yahoo Finance
- **P/E Ratios**: Calculated using current prices and EPS
- **P/B Ratios**: Calculated using current prices and Book Value
- **Volume**: Trading volume data
- **Date**: Updated to current trading date

## Data Sources

- **Primary**: Yahoo Finance API (free, reliable)
- **Symbols**: NSE-listed stocks (RELIANCE.NS, TCS.NS, etc.)
- **Fallback**: Sample data if API fails

## Monitoring

Check if updates are working:
```bash
# View recent logs
tail -f /tmp/market_updates.log

# Test current data
curl http://localhost:8000/screener?limit=3
```

## Troubleshooting

1. **If cron doesn't work:**
   - Check if the script path is correct
   - Ensure the script has execute permissions
   - Check the log file for errors

2. **If API fails:**
   - The script will use fallback data
   - Check internet connection
   - Verify Yahoo Finance API is accessible

3. **If data seems old:**
   - Run manual update: `python api/fetch_real_market_data.py`
   - Check the database: `python -c "from api.database import engine; from sqlmodel import Session, select; from api.models.core import PriceEOD; session = Session(engine); result = session.exec(select(PriceEOD).order_by(PriceEOD.trade_date.desc()).limit(1)); print(f'Latest data: {result.first().trade_date}')"`

## Production Setup

For production, consider:
- **Docker containers** with scheduled tasks
- **Cloud functions** (AWS Lambda, Google Cloud Functions)
- **Message queues** (Redis, RabbitMQ)
- **Monitoring** (Prometheus, Grafana)
- **Alerting** for failed updates 