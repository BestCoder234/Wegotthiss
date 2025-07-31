import os
import sys
from datetime import datetime, date
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import engine

def update_fundamentals():
    """
    Update fundamental data to match current market prices
    """
    
    # Updated fundamental data with more realistic EPS and Book Value
    fundamental_data = [
        {"symbol": "RELIANCE", "eps": 95.0, "book_value": 1350.0},
        {"symbol": "TCS", "eps": 140.0, "book_value": 800.0},
        {"symbol": "INFY", "eps": 70.0, "book_value": 320.0},
        {"symbol": "HDFCBANK", "eps": 85.0, "book_value": 420.0},
        {"symbol": "ICICIBANK", "eps": 50.0, "book_value": 270.0},
        {"symbol": "HINDUNILVR", "eps": 28.0, "book_value": 160.0},
        {"symbol": "ITC", "eps": 18.0, "book_value": 110.0},
        {"symbol": "SBIN", "eps": 38.0, "book_value": 220.0},
        {"symbol": "BHARTIARTL", "eps": 10.0, "book_value": 55.0},
        {"symbol": "AXISBANK", "eps": 35.0, "book_value": 190.0},
    ]
    
    fiscal_year = date.today().year
    
    # Prepare data for database
    data_to_insert = []
    for stock in fundamental_data:
        data_to_insert.append({
            'symbol': stock['symbol'],
            'fiscal_year': fiscal_year,
            'eps': stock['eps'],
            'book_value': stock['book_value']
        })
    
    # Create insert statement
    from sqlalchemy import Table, MetaData
    metadata = MetaData()
    table = Table('fundamentals', metadata, autoload_with=engine)
    
    insert_stmt = insert(table).values(data_to_insert)
    
    # Execute the insert
    with engine.connect() as conn:
        # First, delete any existing data for this fiscal year
        delete_stmt = text(f"DELETE FROM fundamentals WHERE fiscal_year = {fiscal_year}")
        conn.execute(delete_stmt)
        
        # Then insert new data
        result = conn.execute(insert_stmt)
        conn.commit()
    
    print(f"✅ Updated {len(data_to_insert)} fundamental records for fiscal year {fiscal_year}")
    return len(data_to_insert)

if __name__ == "__main__":
    update_fundamentals() 