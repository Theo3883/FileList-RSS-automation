#!/usr/bin/env python3
"""
FileList RSS Handler Entry Point
Run this file to start the application
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from filelist_handler.main import FileListHandler


def main():
    """Main entry point"""
    handler = FileListHandler()
    handler.run()


if __name__ == '__main__':
    main()

