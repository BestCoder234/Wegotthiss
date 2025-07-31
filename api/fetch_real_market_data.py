import os
import sys
import requests
import pandas as pd
from datetime import datetime, date
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import engine

def fetch_real_market_data():
    """
    Fetch real market data from Yahoo Finance API
    """
    
    # Indian stock symbols with .NS suffix for NSE
    symbols = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "AXISBANK.NS"
    ]
    
    current_data = []
    
    for symbol in symbols:
        try:
            # Yahoo Finance API endpoint
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                'range': '1d',
                'interval': '1d',
                'includePrePost': 'false'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                meta = result.get('meta', {})
                indicators = result.get('indicators', {})
                
                # Extract price data
                if 'quote' in indicators and indicators['quote']:
                    quote = indicators['quote'][0]
                    open_price = quote.get('open', [None])[-1]
                    high_price = quote.get('high', [None])[-1]
                    low_price = quote.get('low', [None])[-1]
                    close_price = quote.get('close', [None])[-1]
                    volume = quote.get('volume', [0])[-1]
                    
                    if close_price is not None:
                        # Remove .NS suffix for database
                        clean_symbol = symbol.replace('.NS', '')
                        
                        current_data.append({
                            'symbol': clean_symbol,
                            'open': open_price or close_price,
                            'high': high_price or close_price,
                            'low': low_price or close_price,
                            'close': close_price,
                            'volume': volume or 0
                        })
                        
                        print(f"✅ {clean_symbol}: ₹{close_price}")
                    else:
                        print(f"❌ {symbol}: No price data available")
                else:
                    print(f"❌ {symbol}: No quote data available")
            else:
                print(f"❌ {symbol}: Invalid response format")
                
        except Exception as e:
            print(f"❌ Error fetching {symbol}: {str(e)}")
            continue
    
    if not current_data:
        print("❌ No market data could be fetched. Using fallback data.")
        # Fallback to sample data if API fails
        current_data = [
            {"symbol": "RELIANCE", "close": 2850.0, "open": 2820.0, "high": 2870.0, "low": 2810.0, "volume": 1500000},
            {"symbol": "TCS", "close": 3950.0, "open": 3920.0, "high": 3980.0, "low": 3910.0, "volume": 800000},
            {"symbol": "INFY", "close": 1650.0, "open": 1630.0, "high": 1670.0, "low": 1625.0, "volume": 1200000},
            {"symbol": "HDFCBANK", "close": 1750.0, "open": 1730.0, "high": 1765.0, "low": 1725.0, "volume": 900000},
            {"symbol": "ICICIBANK", "close": 1050.0, "open": 1040.0, "high": 1060.0, "low": 1035.0, "volume": 1100000},
        ]
    
    today = date.today()
    
    # Prepare data for database
    data_to_insert = []
    for stock in current_data:
        data_to_insert.append({
            'symbol': stock['symbol'],
            'trade_date': today,
            'open': stock['open'],
            'high': stock['high'],
            'low': stock['low'],
            'close': stock['close'],
            'volume': stock['volume']
        })
    
    # Create insert statement
    from sqlalchemy import Table, MetaData
    metadata = MetaData()
    table = Table('prices_eod', metadata, autoload_with=engine)
    
    insert_stmt = insert(table).values(data_to_insert)
    
    # Execute the insert
    with engine.connect() as conn:
        # First, delete any existing data for today
        delete_stmt = text(f"DELETE FROM prices_eod WHERE trade_date = '{today}'")
        conn.execute(delete_stmt)
        
        # Then insert new data
        result = conn.execute(insert_stmt)
        conn.commit()
    
    print(f"✅ Updated {len(data_to_insert)} stock prices for {today}")
    return len(data_to_insert)

if __name__ == "__main__":
    fetch_real_market_data() 