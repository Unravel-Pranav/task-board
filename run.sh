#!/bin/bash

echo "🚀 Starting Task Board Application..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install fastapi uvicorn pydantic --quiet

# Check if frontend needs building
if [ ! -d "frontend/dist" ]; then
    echo "🔨 Building frontend..."
    cd frontend
    npm install --silent
    npm run build
    cd ..
else
    echo "✅ Frontend already built"
fi

# Start the server
echo "🌐 Starting server on port 8000..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

