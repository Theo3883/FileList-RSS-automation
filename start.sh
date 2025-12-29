#!/bin/bash

# FileList RSS Handler - Startup Script

echo "=================================================================="
echo "FileList RSS Handler - Startup"
echo "=================================================================="
echo ""

# Check if qBittorrent-nox is running
echo "→ Checking qBittorrent-nox status..."
if ! pgrep -x "qbittorrent-nox" > /dev/null; then
    echo "⚠  qBittorrent-nox is not running!"
    echo ""
    echo "Starting qBittorrent-nox..."
    sudo rc-service qbittorrent-nox start
    
    if [ $? -eq 0 ]; then
        echo "✓ qBittorrent-nox started successfully"
        echo "  Waiting 3 seconds for it to initialize..."
        sleep 3
    else
        echo "✗ Failed to start qBittorrent-nox"
        echo ""
        echo "Please start it manually:"
        echo "  sudo rc-service qbittorrent-nox start"
        exit 1
    fi
else
    echo "✓ qBittorrent-nox is running"
fi

echo ""

# Test connection
echo "→ Testing qBittorrent connection..."
python3 test_connection.py

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ Connection test failed. Please fix the issues above."
    exit 1
fi

# Start the application
echo "→ Starting FileList RSS Handler..."
echo ""

# Check if already running
if pgrep -f "run.py" > /dev/null; then
    echo "⚠  FileList Handler is already running!"
    echo ""
    echo "To stop it:"
    echo "  pkill -f run.py"
    echo ""
    echo "Or view its logs:"
    echo "  tail -f filelist_handler.log"
    exit 0
fi

# Start in background
nohup python3 run.py > /dev/null 2>&1 &
PID=$!

sleep 2

if ps -p $PID > /dev/null; then
    echo "✓ FileList Handler started successfully!"
    echo "  PID: $PID"
    echo ""
    echo "Monitor logs:"
    echo "  tail -f filelist_handler.log"
    echo ""
    echo "Stop the handler:"
    echo "  kill $PID"
    echo "  # or"
    echo "  pkill -f run.py"
    echo ""
else
    echo "✗ Failed to start FileList Handler"
    echo ""
    echo "Check the logs for errors:"
    echo "  tail -50 filelist_handler.log"
    exit 1
fi

