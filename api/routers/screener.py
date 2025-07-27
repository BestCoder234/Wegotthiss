from fastapi import APIRouter, Query
from sqlmodel import Session, select
from models.core import PriceEOD, Fundamental
from database import engine  # assume you load DATABASE_URL in api/database.py

router = APIRouter()

@router.get("/screener")
async def screener(
    pe: float | None = Query(None),
    pb: float | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    with Session(engine) as session:
        stmt = (
            select( Fundamental.symbol,
                    (PriceEOD.close / Fundamental.eps).label("pe"),
                    (PriceEOD.close / Fundamental.book_value).label("pb"),
                    PriceEOD.close,
                    Fundamental.eps,
                    Fundamental.book_value,
            )
            .join(PriceEOD, Fundamental.symbol == PriceEOD.symbol)
        )
        if pe is not None:
            stmt = stmt.where((PriceEOD.close / Fundamental.eps) <= pe)
        if pb is not None:
            stmt = stmt.where((PriceEOD.close / Fundamental.book_value) <= pb)
        results = session.exec(stmt.offset(offset).limit(limit)).all()
        return [ r._asdict() for r in results ] 