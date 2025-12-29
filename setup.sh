#!/bin/bash

# FileList RSS Handler Setup Script

echo "=================================="
echo "FileList RSS Handler Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi

# Create virtual environment (optional but recommended)
echo ""
read -p "Create virtual environment? (recommended) [Y/n]: " create_venv
create_venv=${create_venv:-Y}

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Virtual environment activated!"
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies!"
    exit 1
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit config.yml and add your FileList API key"
echo "2. Configure your torrent client settings"
echo "3. Run: python rss_handler.py"
echo ""

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Note: Remember to activate virtual environment:"
    echo "      source venv/bin/activate"
    echo ""
fi

echo "For systemd service installation:"
echo "      sudo cp filelist-handler.service /etc/systemd/system/"
echo "      sudo systemctl enable filelist-handler"
echo "      sudo systemctl start filelist-handler"
echo ""

