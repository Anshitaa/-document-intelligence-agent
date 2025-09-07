#!/bin/bash
# Document Intelligence Agent - Web UI Launcher

echo "🚀 Document Intelligence Agent - Web Interface"
echo "=============================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

# Check if requirements are installed
echo "🔍 Checking requirements..."
python -c "import streamlit, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing requirements. Installing..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found"
    echo "Please create .env file with your OpenAI API key:"
    echo "echo 'OPENAI_API_KEY=your_key_here' > .env"
    exit 1
fi

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "❌ data directory not found"
    echo "Please create data directory and add PDF files:"
    echo "mkdir data"
    echo "cp your_documents.pdf data/"
    exit 1
fi

echo "✅ All checks passed!"
echo "🌐 Starting web interface..."
echo "📱 Open your browser to: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the server"
echo "----------------------------------------"

# Launch the web app
python run_web_app.py
