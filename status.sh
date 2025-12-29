#!/bin/bash

# FileList RSS Handler - Status Check

echo "=================================================================="
echo "FileList RSS Handler - Status"
echo "=================================================================="
echo ""

# Check qBittorrent-nox
echo "→ qBittorrent-nox:"
if pgrep -x "qbittorrent-nox" > /dev/null; then
    echo "  ✓ Running"
    rc-service qbittorrent-nox status 2>/dev/null | grep -E "(started|running)" || echo "    PID: $(pgrep -x qbittorrent-nox)"
else
    echo "  ✗ Not running"
    echo "    Start with: sudo rc-service qbittorrent-nox start"
fi

echo ""

# Check FileList Handler
echo "→ FileList Handler:"
if pgrep -f "run.py" > /dev/null; then
    PID=$(pgrep -f "run.py")
    echo "  ✓ Running"
    echo "    PID: $PID"
    
    # Show last few log lines
    if [ -f "filelist_handler.log" ]; then
        echo ""
        echo "  Last activity:"
        tail -5 filelist_handler.log | sed 's/^/    /'
    fi
else
    echo "  ✗ Not running"
    echo "    Start with: ./start.sh"
fi

echo ""

# Check database
echo "→ Database:"
if [ -f "torrents.json" ]; then
    COUNT=$(python3 -c "import json; data=json.load(open('torrents.json')); print(len(data))" 2>/dev/null || echo "0")
    echo "  ✓ torrents.json exists"
    echo "    Tracked torrents: $COUNT"
else
    echo "  → No database yet (will be created on first run)"
fi

echo ""

# Check logs
echo "→ Logs:"
if [ -f "filelist_handler.log" ]; then
    SIZE=$(du -h filelist_handler.log | cut -f1)
    LINES=$(wc -l < filelist_handler.log)
    echo "  ✓ filelist_handler.log exists"
    echo "    Size: $SIZE, Lines: $LINES"
else
    echo "  → No logs yet"
fi

echo ""
echo "=================================================================="
echo "Commands:"
echo "  Start:   ./start.sh"
echo "  Stop:    ./stop.sh"
echo "  Logs:    tail -f filelist_handler.log"
echo "  Test:    python3 test_connection.py"
echo "=================================================================="

