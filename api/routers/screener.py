from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from ..models.core import PriceEOD, Fundamental
from ..database import engine
import csv
import io
import xlsxwriter
from typing import List

router = APIRouter()

def get_screener_data(session: Session, pe: float | None = None, pb: float | None = None, 
                     industry: str | None = None, limit: int = 50, offset: int = 0):
    """Helper function to get screener data with filters"""
    # Get the latest trade date
    latest_date_stmt = select(PriceEOD.trade_date).order_by(PriceEOD.trade_date.desc()).limit(1)
    latest_date = session.exec(latest_date_stmt).first()
    
    stmt = (
        select( Fundamental.symbol,
                (PriceEOD.close / Fundamental.eps).label("pe"),
                (PriceEOD.close / Fundamental.book_value).label("pb"),
                PriceEOD.close,
                Fundamental.eps,
                Fundamental.book_value,
                Fundamental.industry,
        )
        .join(PriceEOD, Fundamental.symbol == PriceEOD.symbol)
        .where(PriceEOD.trade_date == latest_date)
    )
    if pe is not None:
        stmt = stmt.where((PriceEOD.close / Fundamental.eps) <= pe)
    if pb is not None:
        stmt = stmt.where((PriceEOD.close / Fundamental.book_value) <= pb)
    if industry is not None:
        stmt = stmt.where(Fundamental.industry == industry)
    
    results = session.exec(stmt.offset(offset).limit(limit)).all()
    return [r._asdict() for r in results]

@router.get("/screener")
async def screener(
    pe: float | None = Query(None),
    pb: float | None = Query(None),
    industry: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    with Session(engine) as session:
        return get_screener_data(session, pe, pb, industry, limit, offset)

@router.get("/screener/export.csv")
async def export_csv(
    pe: float | None = Query(None),
    pb: float | None = Query(None),
    industry: str | None = Query(None),
):
    def generate_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Symbol', 'P/E Ratio', 'P/B Ratio', 'Close Price', 'EPS', 'Book Value', 'Industry'])
        
        with Session(engine) as session:
            data = get_screener_data(session, pe, pb, industry, limit=1000, offset=0)
            for row in data:
                writer.writerow([
                    row['symbol'],
                    f"{row['pe']:.2f}" if row['pe'] else '',
                    f"{row['pb']:.2f}" if row['pb'] else '',
                    f"{row['close']:.2f}" if row['close'] else '',
                    f"{row['eps']:.2f}" if row['eps'] else '',
                    f"{row['book_value']:.2f}" if row['book_value'] else '',
                    row.get('industry', '')
                ])
        
        output.seek(0)
        return output.getvalue()
    
    return StreamingResponse(
        io.StringIO(generate_csv()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=screener.csv"}
    )

@router.get("/screener/export.xlsx")
async def export_xlsx(
    pe: float | None = Query(None),
    pb: float | None = Query(None),
    industry: str | None = Query(None),
):
    def generate_xlsx():
        output = io.BytesIO()
        
        with xlsxwriter.Workbook(output) as workbook:
            worksheet = workbook.add_worksheet()
            
            # Add formats
            header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
            number_format = workbook.add_format({'num_format': '#,##0.00'})
            
            # Write header
            headers = ['Symbol', 'P/E Ratio', 'P/B Ratio', 'Close Price', 'EPS', 'Book Value', 'Industry']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)
            
            with Session(engine) as session:
                data = get_screener_data(session, pe, pb, industry, limit=1000, offset=0)
                for row_idx, row in enumerate(data, start=1):
                    worksheet.write(row_idx, 0, row['symbol'])
                    worksheet.write(row_idx, 1, row['pe'], number_format)
                    worksheet.write(row_idx, 2, row['pb'], number_format)
                    worksheet.write(row_idx, 3, row['close'], number_format)
                    worksheet.write(row_idx, 4, row['eps'], number_format)
                    worksheet.write(row_idx, 5, row['book_value'], number_format)
                    worksheet.write(row_idx, 6, row.get('industry', ''))
        
        output.seek(0)
        return output.getvalue()
    
    return StreamingResponse(
        io.BytesIO(generate_xlsx()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=screener.xlsx"}
    )

@router.get("/industries")
async def get_industries():
    """Get list of available industries"""
    with Session(engine) as session:
        stmt = select(Fundamental.industry).distinct().where(Fundamental.industry.is_not(None))
        results = session.exec(stmt).all()
        return [industry for industry in results if industry] 