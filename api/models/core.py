from datetime import date
from sqlmodel import SQLModel, Field

class PriceEOD(SQLModel, table=True):
    __tablename__ = "prices_eod"
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    trade_date: date = Field(index=True)
    open: float
    high: float
    low: float
    close: float
    volume: int

class Fundamental(SQLModel, table=True):
    __tablename__ = "fundamentals"
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    fiscal_year: int
    eps: float
    book_value: float
    industry: str | None = Field(default=None) 