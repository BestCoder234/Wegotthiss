import os
import sys
import requests
import pandas as pd
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import engine
from api.models.core import PriceEOD

def update_realtime_data():
    """
    Update stock prices with more recent data
    Using a sample of current market prices for demonstration
    """
    
    # Sample current market data (in a real app, this would come from a live API)
    current_data = [
        {"symbol": "RELIANCE", "close": 2850.0, "open": 2820.0, "high": 2870.0, "low": 2810.0, "volume": 1500000},
        {"symbol": "TCS", "close": 3950.0, "open": 3920.0, "high": 3980.0, "low": 3910.0, "volume": 800000},
        {"symbol": "INFY", "close": 1650.0, "open": 1630.0, "high": 1670.0, "low": 1625.0, "volume": 1200000},
        {"symbol": "HDFCBANK", "close": 1750.0, "open": 1730.0, "high": 1765.0, "low": 1725.0, "volume": 900000},
        {"symbol": "ICICIBANK", "close": 1050.0, "open": 1040.0, "high": 1060.0, "low": 1035.0, "volume": 1100000},
        {"symbol": "HINDUNILVR", "close": 2800.0, "open": 2780.0, "high": 2820.0, "low": 2775.0, "volume": 600000},
        {"symbol": "ITC", "close": 450.0, "open": 445.0, "high": 455.0, "low": 443.0, "volume": 2000000},
        {"symbol": "SBIN", "close": 750.0, "open": 745.0, "high": 755.0, "low": 743.0, "volume": 1500000},
        {"symbol": "BHARTIARTL", "close": 1200.0, "open": 1190.0, "high": 1210.0, "low": 1185.0, "volume": 800000},
        {"symbol": "AXISBANK", "close": 1100.0, "open": 1090.0, "high": 1110.0, "low": 1085.0, "volume": 1000000},
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
    
    # Create insert statement with conflict resolution
    from sqlalchemy import Table, MetaData
    metadata = MetaData()
    table = Table('prices_eod', metadata, autoload_with=engine)
    
    insert_stmt = insert(table).values(data_to_insert)
    
    # Handle conflicts by updating existing records
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=['symbol', 'trade_date'],
        set_={
            'open': insert_stmt.excluded.open,
            'high': insert_stmt.excluded.high,
            'low': insert_stmt.excluded.low,
            'close': insert_stmt.excluded.close,
            'volume': insert_stmt.excluded.volume
        }
    )
    
    # Execute the insert
    with engine.connect() as conn:
        # First, delete any existing data for today
        from sqlalchemy import text
        delete_stmt = text(f"DELETE FROM prices_eod WHERE trade_date = '{today}'")
        conn.execute(delete_stmt)
        
        # Then insert new data
        result = conn.execute(insert_stmt)
        conn.commit()
    
    print(f"✅ Updated {len(data_to_insert)} stock prices for {today}")
    return len(data_to_insert)

if __name__ == "__main__":
    update_realtime_data() 