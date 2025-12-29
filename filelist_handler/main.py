"""Main application logic"""

import time
import logging
from typing import List

from .config import Config
from .models import Torrent, TorrentStatus
from .parsers import RSSFeedParser
from .storage import StorageManager, TorrentRepository
from .factories import TorrentClientFactory
from .observers import Subject, LoggingObserver


class FileListHandler(Subject):
    """Main handler for FileList torrent management"""
    
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.setup_logging()
        
        # Attach logging observer
        self.attach(LoggingObserver())
        
        # Initialize components
        self.rss_parser = RSSFeedParser(self.config.rss_feed_url)
        self.torrent_client = TorrentClientFactory.create_client(self.config)
        self.storage_manager = StorageManager(
            self.config.get('storage.download_path'),
            self.config.get('storage.max_size_gb')
        )
        self.repository = TorrentRepository(
            self.config.get('storage.torrents_db', 'torrents.json')
        )
        
        # Get max torrents per run
        self.max_torrents_per_run = self.config.get('filelist.max_torrents_per_run', 5)
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_level = self.config.get('logging.level', 'INFO')
        log_file = self.config.get('logging.file', 'filelist_handler.log')
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def should_download(self, torrent: Torrent) -> bool:
        """Check if torrent meets download criteria"""
        # Check if already exists
        if self.repository.exists(torrent.id):
            return False
        
        # Check freeleech requirement
        if self.config.get('filters.freeleech_only') and not torrent.is_freeleech:
            return False
        
        # Check minimum seeders
        min_seeders = self.config.get('filters.min_seeders', 0)
        if torrent.seeders < min_seeders:
            return False
        
        return True
    
    def cleanup_storage(self, required_space: int = 0):
        """Remove old torrents to free up space"""
        while self.storage_manager.needs_cleanup(required_space):
            all_torrents = self.repository.get_all()
            oldest = self.storage_manager.get_oldest_torrents(all_torrents, count=1)
            
            if not oldest:
                self.notify('error', {'message': 'No torrents available for cleanup'})
                break
            
            torrent = oldest[0]
            
            # Mark as deleted in repository
            torrent.status = TorrentStatus.DELETED
            self.repository.update(torrent)
            
            self.notify('torrent_deleted', {
                'title': torrent.title,
                'size_mb': torrent.size / (1024**2)
            })
    
    def process_feed(self):
        """Process RSS feed and download freeleech torrents"""
        logging.info("=" * 70)
        logging.info("Starting FileList RSS check...")
        
        # Fetch RSS feed
        entries = self.rss_parser.fetch_entries()
        
        if not entries:
            logging.warning("No entries found in RSS feed")
            return
        
        # Count freeleech torrents
        freeleech_count = sum(1 for e in entries if '[FreeLeech]' in e.get('title', ''))
        
        self.notify('feed_check', {
            'total': len(entries),
            'freeleech': freeleech_count
        })
        
        # Track downloads this run
        downloaded_count = 0
        
        # Process each entry
        for entry in entries:
            # Stop if we've reached the limit
            if downloaded_count >= self.max_torrents_per_run:
                logging.info(f"✓ Reached limit of {self.max_torrents_per_run} torrents per run")
                break
            
            torrent = self.rss_parser.parse_entry(entry)
            if not torrent:
                continue
            
            # Check if should download
            if not self.should_download(torrent):
                continue
            
            # Check if we need to cleanup before downloading
            self.cleanup_storage(required_space=torrent.size)
            
            # Add torrent to client
            download_path = self.config.get('storage.download_path')
            if self.torrent_client.add_torrent(torrent.link, download_path):
                torrent.status = TorrentStatus.DOWNLOADING
                self.repository.add(torrent)
                
                self.notify('torrent_added', {
                    'title': torrent.title,
                    'size_mb': torrent.size / (1024**2),
                    'category': torrent.category
                })
                
                downloaded_count += 1
            else:
                self.notify('error', {
                    'message': f"Failed to add torrent: {torrent.title}"
                })
        
        if downloaded_count == 0:
            logging.info("→ No new torrents to download")
        
        # Show storage status
        usage = self.storage_manager.get_usage_percent()
        logging.info(f"→ Storage usage: {usage:.1f}%")
        
        logging.info("✓ RSS check completed")
        logging.info("=" * 70)
    
    def run(self):
        """Main run loop"""
        check_interval = self.config.get('filelist.check_interval', 300)
        
        logging.info("=" * 70)
        logging.info("FileList RSS Handler Started")
        logging.info("=" * 70)
        logging.info(f"RSS URL: {self.config.rss_feed_url[:50]}...")
        logging.info(f"Check interval: {check_interval} seconds ({check_interval//60} minutes)")
        logging.info(f"Max storage: {self.config.get('storage.max_size_gb')} GB")
        logging.info(f"Freeleech only: {self.config.get('filters.freeleech_only')}")
        logging.info(f"Torrents per run: {self.max_torrents_per_run}")
        logging.info(f"Download path: {self.config.get('storage.download_path')}")
        logging.info("=" * 70)
        
        try:
            while True:
                try:
                    self.process_feed()
                except Exception as e:
                    self.notify('error', {'message': str(e)})
                    logging.exception("Error processing feed")
                
                logging.info(f"\n💤 Sleeping for {check_interval} seconds...\n")
                time.sleep(check_interval)
        except KeyboardInterrupt:
            logging.info("\n👋 Shutting down gracefully...")

