from dagster import op
import pandas as pd
from datetime import datetime, timedelta
import pytz
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
import os

@op
def test_bhavcopy():
    """
    Test version that inserts sample data instead of downloading from NSE
    """
    # Create sample data
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    yesterday = datetime.now(kolkata_tz) - timedelta(days=1)
    
    # Sample data for popular Indian stocks
    sample_data = [
        {'symbol': 'RELIANCE', 'trade_date': yesterday.date(), 'open': 2500.0, 'high': 2550.0, 'low': 2480.0, 'close': 2520.0, 'volume': 1000000},
        {'symbol': 'TCS', 'trade_date': yesterday.date(), 'open': 3800.0, 'high': 3850.0, 'low': 3780.0, 'close': 3820.0, 'volume': 500000},
        {'symbol': 'INFY', 'trade_date': yesterday.date(), 'open': 1500.0, 'high': 1520.0, 'low': 1490.0, 'close': 1510.0, 'volume': 800000},
        {'symbol': 'HDFCBANK', 'trade_date': yesterday.date(), 'open': 1600.0, 'high': 1620.0, 'low': 1590.0, 'close': 1610.0, 'volume': 600000},
        {'symbol': 'ICICIBANK', 'trade_date': yesterday.date(), 'open': 950.0, 'high': 970.0, 'low': 940.0, 'close': 960.0, 'volume': 700000},
    ]
    
    df = pd.DataFrame(sample_data)
    
    # Create SQLAlchemy engine
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:devpass@localhost:5432/screener")
    engine = create_engine(database_url)
    
    # Upsert data to prices_eod table
    from sqlalchemy import Table, MetaData
    
    metadata = MetaData()
    table = Table('prices_eod', metadata, autoload_with=engine)
    data_to_insert = df.to_dict('records')
    
    # Execute the insert
    with engine.connect() as conn:
        result = conn.execute(insert(table).values(data_to_insert))
        conn.commit()
    
    return len(data_to_insert) 