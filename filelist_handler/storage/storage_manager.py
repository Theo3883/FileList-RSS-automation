"""Storage manager for handling disk space"""

import logging
from pathlib import Path
from typing import List
from ..models import Torrent, TorrentStatus


class StorageManager:
    """Manages storage and enforces size limits"""
    
    def __init__(self, download_path: str, max_size_gb: float):
        self.download_path = Path(download_path)
        self.max_size_bytes = int(max_size_gb * 1024**3)
    
    def get_folder_size(self) -> int:
        """Calculate total size of download folder"""
        total_size = 0
        try:
            if not self.download_path.exists():
                return 0
            for item in self.download_path.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
        except Exception as e:
            logging.error(f"Failed to calculate folder size: {e}")
        return total_size
    
    def needs_cleanup(self, additional_size: int = 0) -> bool:
        """Check if cleanup is needed"""
        current_size = self.get_folder_size()
        return (current_size + additional_size) > self.max_size_bytes
    
    def get_oldest_torrents(self, torrents: List[Torrent], count: int = 1) -> List[Torrent]:
        """Get oldest completed torrents"""
        completed = [t for t in torrents if t.status == TorrentStatus.COMPLETED]
        # Sort by completion date (oldest first)
        completed.sort(key=lambda t: t.completed_date or t.added_date)
        return completed[:count]
    
    def get_usage_percent(self) -> float:
        """Get storage usage percentage"""
        current_size = self.get_folder_size()
        return (current_size / self.max_size_bytes) * 100

