import os
import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text, Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from dagster import op
import yfinance as yf

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.database import engine

@op
def download_fundamentals():
    """
    Download fundamental data using yfinance library
    """
    # Define symbols with .NS suffix for NSE
    symbols = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", 
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "AXISBANK.NS"
    ]
    
    rows = []
    fiscal_year = datetime.now().year
    
    for symbol in symbols:
        try:
            print(f"Processing {symbol}...")
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract EPS and Book Value
            eps = info.get("trailingEps") or info.get("earningsPerShare")
            book_value = info.get("bookValue")
            
            if eps and book_value:
                # Remove .NS suffix for database storage
                clean_symbol = symbol.replace(".NS", "")
                rows.append({
                    "symbol": clean_symbol,
                    "fiscal_year": fiscal_year,
                    "eps": eps,
                    "book_value": book_value
                })
                print(f"✅ {clean_symbol}: EPS={eps}, BV={book_value} (yfinance)")
            else:
                print(f"❌ {symbol}: Missing EPS or Book Value data")
                
        except Exception as e:
            print(f"❌ Error processing {symbol}: {str(e)}")
            continue
    
    if not rows:
        print("No fundamental data to insert.")
        return 0
    
    df = pd.DataFrame(rows)
    
    # Insert into database
    metadata = MetaData()
    table = Table('fundamentals', metadata, autoload_with=engine)
    data_to_insert = df.to_dict('records')
    
    insert_stmt = insert(table).values(data_to_insert)
    
    with engine.connect() as conn:
        # First, delete any existing data for this fiscal year
        delete_stmt = text(f"DELETE FROM fundamentals WHERE fiscal_year = {fiscal_year}")
        conn.execute(delete_stmt)
        
        # Then insert new data
        result = conn.execute(insert_stmt)
        conn.commit()
    
    print(f"✅ Inserted {len(data_to_insert)} fundamental records")
    return len(data_to_insert) 