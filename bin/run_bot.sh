#!/bin/bash

# Discord AI Bot - Auto-Restart Script
# Usage: chmod +x run_bot.sh && ./run_bot.sh

echo "🤖 Discord AI Bot - Auto Restart Script"
echo "========================================"
echo ""

# Activate virtual environment
if [ -d "venv/bin" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found! Please create it first:"
    echo "   python -m venv venv"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "   Please create .env file with your tokens"
    exit 1
fi

# Check if bot.py exists
if [ ! -f "bot.py" ]; then
    echo "❌ bot.py not found!"
    exit 1
fi

echo "✅ All files found"
echo ""
echo "🚀 Starting bot..."
echo "   Press Ctrl+C twice to stop"
echo ""

# Auto-restart loop
while true; do
    python bot.py
    
    # Check exit code
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo ""
        echo "✅ Bot exited normally"
        break
    else
        echo ""
        echo "❌ Bot crashed with exit code: $EXIT_CODE"
        echo "🔄 Restarting in 5 seconds..."
        echo "   Press Ctrl+C to cancel"
        sleep 5
    fi
done

echo ""
echo "👋 Bot stopped"