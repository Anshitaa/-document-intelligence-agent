#!/bin/bash
echo "🚀 Installing Document Intelligence Agent..."
pip install -r requirements.txt
echo "✅ Installation complete!"
echo "📝 Next steps:"
echo "   1. Copy .env.example to .env"
echo "   2. Add your OpenAI API key to .env"
echo "   3. Add your PDF files to data/ directory"
echo "   4. Run: python run_web_app.py"
