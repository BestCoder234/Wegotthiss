#!/bin/bash

# Activate Python virtual environment
source .venv/bin/activate

# Install Dagster and related packages
pip install dagster dagster-webserver dagster-postgres pandas requests

# Run Dagster scaffold command
dagster project scaffold -m etl -n screener_etl

echo "ETL scaffold complete!" 