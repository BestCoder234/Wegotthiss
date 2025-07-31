import os
import sys
from sqlalchemy import text

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import engine

def cleanup_old_data():
    """Clean up old fundamental data"""
    with engine.connect() as conn:
        # Delete old fundamental data
        conn.execute(text('DELETE FROM fundamentals WHERE fiscal_year < 2025'))
        conn.commit()
        print('✅ Cleaned old fundamental data')

if __name__ == "__main__":
    cleanup_old_data() 