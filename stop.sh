#!/bin/bash

# FileList RSS Handler - Stop Script

echo "=================================================================="
echo "FileList RSS Handler - Stop"
echo "=================================================================="
echo ""

# Check if running
if ! pgrep -f "run.py" > /dev/null; then
    echo "→ FileList Handler is not running"
    exit 0
fi

echo "→ Stopping FileList Handler..."

# Kill the process
pkill -f "run.py"

# Wait a moment
sleep 2

# Check if stopped
if ! pgrep -f "run.py" > /dev/null; then
    echo "✓ FileList Handler stopped successfully"
else
    echo "⚠  Process still running, forcing kill..."
    pkill -9 -f "run.py"
    sleep 1
    
    if ! pgrep -f "run.py" > /dev/null; then
        echo "✓ FileList Handler force stopped"
    else
        echo "✗ Failed to stop FileList Handler"
        echo "  Please manually kill the process"
        exit 1
    fi
fi

echo ""
echo "To start again:"
echo "  ./start.sh"
echo "  # or"
echo "  python3 run.py"

