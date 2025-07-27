#!/bin/bash

# Create Python virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn[standard] sqlmodel psycopg2-binary python-dotenv pytest httpx

# Create directory structure
mkdir -p api/routers

# Create main.py file
cat > api/main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
async def health():
    return {"status": "ok"}
EOF

echo "API scaffold complete!"
echo ""
echo "To start the server, run:"
echo "uvicorn api.main:app --reload" 