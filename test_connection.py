#!/usr/bin/env python3
"""
Test script to verify qBittorrent-nox connection
Run this to ensure everything is configured correctly before starting the main app
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from filelist_handler.config import Config
from filelist_handler.factories import TorrentClientFactory


def test_connection():
    """Test connection to qBittorrent-nox"""
    print("=" * 70)
    print("Testing qBittorrent-nox Connection")
    print("=" * 70)
    
    try:
        # Load config
        config = Config()
        print(f"✓ Configuration loaded")
        print(f"  Host: {config.get('torrent_client.host')}")
        print(f"  Username: {config.get('torrent_client.username')}")
        print()
        
        # Create client
        print("Connecting to qBittorrent-nox...")
        client = TorrentClientFactory.create_client(config)
        print("✓ Successfully connected to qBittorrent-nox!")
        print()
        
        # Get torrents
        print("Fetching current torrents...")
        torrents = client.get_torrents()
        print(f"✓ Found {len(torrents)} active torrents")
        
        if torrents:
            print("\nCurrent torrents:")
            for i, torrent in enumerate(torrents[:5], 1):
                name = torrent.get('name', 'Unknown')
                state = torrent.get('state', 'Unknown')
                progress = torrent.get('progress', 0) * 100
                print(f"  {i}. {name[:60]}... ({state}, {progress:.1f}%)")
            
            if len(torrents) > 5:
                print(f"  ... and {len(torrents) - 5} more")
        else:
            print("  No active torrents")
        
        print()
        print("=" * 70)
        print("✓ Connection test PASSED!")
        print("=" * 70)
        print()
        print("Ready to run the application:")
        print("  python3 run.py")
        print()
        return True
        
    except ConnectionError as e:
        print()
        print("=" * 70)
        print("✗ Connection test FAILED!")
        print("=" * 70)
        print(f"\nError: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Make sure qBittorrent-nox is running:")
        print("     sudo rc-service qbittorrent-nox status")
        print("     sudo rc-service qbittorrent-nox start")
        print()
        print("  2. Check if Web UI is accessible:")
        print("     curl http://localhost:8080")
        print()
        print("  3. Verify credentials in config.yml:")
        print("     username: admin")
        print("     password: adminadmin")
        print()
        return False
        
    except Exception as e:
        print()
        print("=" * 70)
        print("✗ Unexpected error!")
        print("=" * 70)
        print(f"\nError: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)

