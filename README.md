# Stock Screener Application

A comprehensive stock screening application built with FastAPI, Next.js, and PostgreSQL.

## Features

- **Real-time Stock Data**: Fetches live market data using Yahoo Finance API
- **Fundamental Analysis**: P/E and P/B ratio calculations with real fundamental data
- **Interactive UI**: Modern React frontend with TanStack Table and shadcn/ui components
- **ETL Pipeline**: Dagster-based data processing with automated daily updates
- **Database**: PostgreSQL with Alembic migrations for schema management

## Tech Stack

- **Backend**: FastAPI, SQLModel, PostgreSQL
- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Data Processing**: Dagster, yfinance, pandas
- **Testing**: pytest with automated CI/CD
- **Deployment**: Docker Compose

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/BestCoder234/Wegotthiss.git
   cd Wegotthiss
   ```

2. **Start the database**
   ```bash
   docker-compose up -d
   ```

3. **Apply database migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start the backend**
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Start the frontend**
   ```bash
   cd web
   npm install
   npm run dev
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - Dagster UI: http://localhost:3003

## Testing

Run the test suite:
```bash
PYTHONPATH=. pytest api/tests/
```

## Status

![CI](https://github.com/BestCoder234/Wegotthiss/actions/workflows/test.yml/badge.svg)

## License

MIT License 