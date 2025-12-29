"""Logging observer implementation"""

import logging
from .base import Observer


class LoggingObserver(Observer):
    """Observer that logs events"""
    
    def __init__(self):
        self.logger = logging.getLogger('FileListHandler')
    
    def update(self, event: str, data: dict):
        """Log the event"""
        if event == 'torrent_added':
            self.logger.info(f"✓ Added: {data['title']} ({data['size_mb']:.2f} MB)")
        elif event == 'torrent_completed':
            self.logger.info(f"✓ Completed: {data['title']}")
        elif event == 'torrent_deleted':
            self.logger.warning(f"✗ Deleted: {data['title']} (freed {data['size_mb']:.2f} MB)")
        elif event == 'storage_warning':
            self.logger.warning(f"⚠ Storage at {data['usage_percent']:.1f}% capacity")
        elif event == 'error':
            self.logger.error(f"✗ Error: {data['message']}")
        elif event == 'feed_check':
            self.logger.info(f"→ Checking feed... Found {data['total']} entries, {data['freeleech']} freeleech")

