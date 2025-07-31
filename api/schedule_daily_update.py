import os
import sys
import schedule
import time
from datetime import datetime, date
import subprocess

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def update_market_data():
    """Update market data daily"""
    print(f"🔄 Updating market data at {datetime.now()}")
    
    try:
        # Run the market data fetch script
        result = subprocess.run([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'fetch_real_market_data.py')
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Market data updated successfully")
            print(result.stdout)
        else:
            print("❌ Failed to update market data")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error updating market data: {str(e)}")

def setup_daily_schedule():
    """Set up daily schedule for market data updates"""
    print("📅 Setting up daily market data updates...")
    
    # Schedule update at 6:00 PM IST (after market closes)
    schedule.every().day.at("18:00").do(update_market_data)
    
    # Also run once immediately to get current data
    update_market_data()
    
    print("✅ Daily updates scheduled for 6:00 PM IST")
    print("🔄 Running updates every day...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    setup_daily_schedule() 