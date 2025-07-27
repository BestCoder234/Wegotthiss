#!/usr/bin/env python3
"""
Script to add fundamental data for testing
"""
import os
from sqlmodel import SQLModel, Session
from database import engine
from models.core import Fundamental

def add_fundamentals():
    """Add fundamental data for testing"""
    print("Adding fundamental data...")
    
    # Sample fundamental data
    fundamentals = [
        Fundamental(symbol="RELIANCE", fiscal_year=2024, eps=85.0, book_value=1200.0),
        Fundamental(symbol="TCS", fiscal_year=2024, eps=130.0, book_value=750.0),
        Fundamental(symbol="INFY", fiscal_year=2024, eps=65.0, book_value=300.0),
        Fundamental(symbol="HDFCBANK", fiscal_year=2024, eps=80.0, book_value=400.0),
        Fundamental(symbol="ICICIBANK", fiscal_year=2024, eps=45.0, book_value=250.0),
    ]
    
    with Session(engine) as session:
        for fundamental in fundamentals:
            session.add(fundamental)
        session.commit()
    
    print("✅ Fundamental data added successfully!")

if __name__ == "__main__":
    add_fundamentals() 