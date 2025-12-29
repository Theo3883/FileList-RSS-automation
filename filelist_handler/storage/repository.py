"""Torrent repository for data persistence"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from ..models import Torrent, TorrentStatus


class TorrentRepository:
    """Repository for managing torrent data persistence"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.torrents: Dict[str, Torrent] = {}
        self.load()
    
    def load(self):
        """Load torrents from JSON file"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    self.torrents = {
                        k: Torrent.from_dict(v) for k, v in data.items()
                    }
                logging.info(f"✓ Loaded {len(self.torrents)} torrents from database")
            except Exception as e:
                logging.error(f"Failed to load torrent database: {e}")
    
    def save(self):
        """Save torrents to JSON file"""
        try:
            with open(self.db_path, 'w') as f:
                data = {k: v.to_dict() for k, v in self.torrents.items()}
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save torrent database: {e}")
    
    def add(self, torrent: Torrent):
        """Add a torrent"""
        self.torrents[torrent.id] = torrent
        self.save()
    
    def get(self, torrent_id: str) -> Optional[Torrent]:
        """Get a torrent by ID"""
        return self.torrents.get(torrent_id)
    
    def get_all(self) -> List[Torrent]:
        """Get all torrents"""
        return list(self.torrents.values())
    
    def get_by_status(self, status: TorrentStatus) -> List[Torrent]:
        """Get torrents by status"""
        return [t for t in self.torrents.values() if t.status == status]
    
    def update(self, torrent: Torrent):
        """Update a torrent"""
        if torrent.id in self.torrents:
            self.torrents[torrent.id] = torrent
            self.save()
    
    def delete(self, torrent_id: str):
        """Delete a torrent"""
        if torrent_id in self.torrents:
            del self.torrents[torrent_id]
            self.save()
    
    def exists(self, torrent_id: str) -> bool:
        """Check if torrent exists"""
        return torrent_id in self.torrents

