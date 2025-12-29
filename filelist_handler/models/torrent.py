"""Torrent data model"""

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Optional


class TorrentStatus(Enum):
    """Torrent status enumeration"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    DELETED = "deleted"
    ERROR = "error"


@dataclass
class Torrent:
    """Torrent data model"""
    id: str
    title: str
    link: str
    size: int  # bytes
    is_freeleech: bool
    added_date: datetime
    completed_date: Optional[datetime] = None
    status: TorrentStatus = TorrentStatus.PENDING
    category: Optional[str] = None
    seeders: int = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['added_date'] = self.added_date.isoformat()
        data['completed_date'] = self.completed_date.isoformat() if self.completed_date else None
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Torrent':
        """Create from dictionary"""
        data['added_date'] = datetime.fromisoformat(data['added_date'])
        data['completed_date'] = datetime.fromisoformat(data['completed_date']) if data['completed_date'] else None
        data['status'] = TorrentStatus(data['status'])
        return cls(**data)

