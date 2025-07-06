#!/bin/bash

# GitHub Stats SVG API Startup Script

echo "🚀 Starting GitHub Stats SVG API..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Check if .env file exists, if not copy from example
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file to add your GitHub token for better rate limits"
fi

# Start the API
echo "🌟 Starting the API server..."
echo "📍 API will be available at: http://localhost:8000"
echo "📖 API documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
