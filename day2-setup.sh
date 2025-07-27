#!/bin/bash

echo "🚀 Starting Day 2 setup..."

# Execute API scaffold
echo "📦 Setting up FastAPI..."
./scaffold-api.sh

# Execute ETL scaffold
echo "📊 Setting up ETL pipeline..."
./scaffold-etl.sh

# Wait a moment for services to start
echo "⏳ Waiting for API to start..."
sleep 5

# Check health endpoint
echo "🏥 Checking API health..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/healthz)

if [ "$HEALTH_RESPONSE" = '{"status":"ok"}' ]; then
    echo "✅ Day 2 scaffolds complete"
    exit 0
else
    echo "❌ Health check failed. Expected: {\"status\":\"ok\"}, Got: $HEALTH_RESPONSE"
    exit 1
fi 