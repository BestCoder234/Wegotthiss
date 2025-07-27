#!/bin/bash

# Initialize git repo and cd into it
git init screener-2.0
cd screener-2.0

# Create directories
mkdir -p api etl web migrations docs

# Write "16" to .tool-versions
echo "16" > .tool-versions

# Write "v20.11.1" to .nvmrc
echo "v20.11.1" > .nvmrc

# Append "node_modules/" to .gitignore
echo "node_modules/" >> .gitignore

# Stage all changes and commit
git add .
git commit -m "chore: repo scaffold"

echo "Repository setup complete!"
echo ""
echo "To start the database and adminer services, run:"
echo "docker compose up -d" 