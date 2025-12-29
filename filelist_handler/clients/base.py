"""Base torrent client interface (Strategy Pattern)"""

from abc import ABC, abstractmethod
from typing import List, Dict


class TorrentClient(ABC):
    """Abstract torrent client interface"""
    
    @abstractmethod
    def add_torrent(self, torrent_url: str, save_path: str) -> bool:
        """Add a torrent to the client"""
        pass
    
    @abstractmethod
    def get_torrents(self) -> List[Dict]:
        """Get list of torrents from client"""
        pass
    
    @abstractmethod
    def remove_torrent(self, torrent_hash: str, delete_files: bool = True) -> bool:
        """Remove a torrent from client"""
        pass

