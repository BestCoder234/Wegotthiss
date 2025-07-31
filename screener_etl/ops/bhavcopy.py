from dagster import op
import requests
import zipfile
import io
import pandas as pd
from datetime import datetime, timedelta
import pytz
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
import os

@op
def download_bhavcopy():
    """
    Download NSE Bhavcopy ZIP and parse into a pandas DataFrame
    """
    # Compute yesterday's date in Asia/Kolkata timezone
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    yesterday = datetime.now(kolkata_tz) - timedelta(days=1)
    
    # Format the NSE Bhavcopy URL
    year = yesterday.strftime('%Y')
    month = yesterday.strftime('%b').upper()
    day = yesterday.strftime('%d')
    
    url = f"https://www1.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{day}{month}{year}bhav.csv.zip"
    
    # Download the ZIP file
    response = requests.get(url)
    response.raise_for_status()
    
    # Extract CSV from ZIP
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        csv_filename = zip_file.namelist()[0]
        with zip_file.open(csv_filename) as csv_file:
            df = pd.read_csv(csv_file)
    
    # Filter rows where SERIES == "EQ"
    df = df[df['SERIES'] == 'EQ']
    
    # Rename columns to lowercase
    column_mapping = {
        'SYMBOL': 'symbol',
        'TIMESTAMP': 'trade_date',
        'OPEN': 'open',
        'HIGH': 'high',
        'LOW': 'low',
        'CLOSE': 'close',
        'TOTTRDQTY': 'volume'
    }
    df = df.rename(columns=column_mapping)
    
    # Select only the required columns
    df = df[['symbol', 'trade_date', 'open', 'high', 'low', 'close', 'volume']]
    
    # Convert trade_date to datetime
    df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date
    
    # Create SQLAlchemy engine
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    
    # Upsert data to prices_eod table
    table_name = 'prices_eod'
    
    # Prepare data for upsert
    data_to_insert = df.to_dict('records')
    
    # Create insert statement with conflict resolution
    insert_stmt = insert(table_name).values(data_to_insert)
    
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
    
    # Execute the upsert
    with engine.connect() as conn:
        result = conn.execute(upsert_stmt)
        conn.commit()
    
    return len(data_to_insert) 