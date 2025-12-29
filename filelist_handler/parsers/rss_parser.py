"""FileList RSS feed parser"""

import re
import logging
import feedparser
from datetime import datetime
from typing import List, Optional
from ..models import Torrent


class RSSFeedParser:
    """Parser for FileList RSS feeds"""
    
    def __init__(self, feed_url: str):
        self.feed_url = feed_url
    
    def fetch_entries(self) -> List[dict]:
        """Fetch and parse RSS feed entries"""
        try:
            feed = feedparser.parse(self.feed_url)
            return feed.entries
        except Exception as e:
            logging.error(f"Failed to fetch RSS feed: {e}")
            return []
    
    def parse_entry(self, entry: dict) -> Optional[Torrent]:
        """Parse RSS entry into Torrent object"""
        try:
            # Extract basic information
            title = entry.get('title', '')
            link = entry.get('link', '')
            description = entry.get('description', '')
            
            # Check if freeleech (must have [FreeLeech] in title)
            is_freeleech = '[FreeLeech]' in title or '[FREELEECH]' in title.upper()
            
            # Extract size from description
            size_bytes = self._extract_size(description)
            
            # Extract category from description
            category = self._extract_category(description)
            
            # Extract torrent ID from link
            torrent_id = self._extract_id(link)
            
            if not torrent_id:
                logging.warning(f"Could not extract ID from: {link}")
                return None
            
            return Torrent(
                id=torrent_id,
                title=title,
                link=link,
                size=size_bytes,
                is_freeleech=is_freeleech,
                added_date=datetime.now(),
                category=category,
                seeders=0
            )
        except Exception as e:
            logging.error(f"Failed to parse entry: {e}")
            return None
    
    def _extract_id(self, link: str) -> Optional[str]:
        """Extract torrent ID from download link"""
        # Link format: https://filelist.io/download.php?id=946514&passkey=...
        match = re.search(r'id=(\d+)', link)
        return match.group(1) if match else None
    
    def _extract_size(self, description: str) -> int:
        """Extract size from description (in bytes)"""
        # Description format: "Category: ... Size: 32.21 GB ..."
        size_pattern = r'Size:\s*(\d+(?:\.\d+)?)\s*(GB|MB|KB|TB)'
        match = re.search(size_pattern, description, re.IGNORECASE)
        
        if match:
            value = float(match.group(1))
            unit = match.group(2).upper()
            
            multipliers = {
                'KB': 1024,
                'MB': 1024**2,
                'GB': 1024**3,
                'TB': 1024**4
            }
            return int(value * multipliers.get(unit, 1))
        
        return 0  # Unknown size
    
    def _extract_category(self, description: str) -> Optional[str]:
        """Extract category from description"""
        # Description format: "Category: Filme HD ..."
        category_pattern = r'Category:\s*([^\n]+)'
        match = re.search(category_pattern, description)
        return match.group(1).strip() if match else None

