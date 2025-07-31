#!/usr/bin/env python3
"""
Script to create database tables using SQLModel metadata
"""
import os
from sqlmodel import SQLModel
from database import engine
from models.core import PriceEOD, Fundamental

def create_tables():
    """Create all tables defined in SQLModel metadata"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    create_tables() 