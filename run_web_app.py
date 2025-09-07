#!/usr/bin/env python3
"""
Web App Launcher for Document Intelligence Agent
===============================================

This script launches the Streamlit web interface for the Document Intelligence Agent.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed."""
    try:
        import streamlit
        import plotly
        from document_intelligence_agent import DocumentIntelligenceAgent
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if environment is properly set up."""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("Please create .env file with your OpenAI API key:")
        print("echo 'OPENAI_API_KEY=your_key_here' > .env")
        return False
    
    if not os.path.exists("data"):
        print("❌ data directory not found")
        print("Please create data directory and add PDF files:")
        print("mkdir data")
        print("cp your_documents.pdf data/")
        return False
    
    return True

def main():
    """Launch the web application."""
    print("🚀 Document Intelligence Agent - Web Interface")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("🌐 Starting web interface...")
    print("📱 Open your browser to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Launch Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped")
    except Exception as e:
        print(f"❌ Error launching web interface: {e}")

if __name__ == "__main__":
    main()
