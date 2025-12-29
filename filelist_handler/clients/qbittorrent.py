"""qBittorrent Web API client"""

import logging
import requests
from typing import List, Dict
from .base import TorrentClient


class QBittorrentClient(TorrentClient):
    """qBittorrent Web API client"""
    
    def __init__(self, host: str, username: str, password: str):
        self.host = host.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._login()
    
    def _login(self):
        """Login to qBittorrent"""
        try:
            response = self.session.post(
                f"{self.host}/api/v2/auth/login",
                data={'username': self.username, 'password': self.password}
            )
            response.raise_for_status()
            
            # Check if login was successful
            if response.text.strip() == 'Ok.':
                logging.info("✓ Connected to qBittorrent")
            else:
                raise ConnectionError(f"Login failed: {response.text}")
        except Exception as e:
            raise ConnectionError(f"Failed to login to qBittorrent: {e}")
    
    def add_torrent(self, torrent_url: str, save_path: str) -> bool:
        """Add torrent via URL"""
        try:
            response = self.session.post(
                f"{self.host}/api/v2/torrents/add",
                data={'urls': torrent_url, 'savepath': save_path}
            )
            
            # qBittorrent returns 'Ok.' on success
            if response.text.strip() == 'Ok.':
                return True
            else:
                # Log non-Ok responses for debugging
                if response.text.strip() != '':
                    logging.debug(f"qBittorrent add_torrent response: '{response.text}'")
                return False
        except Exception as e:
            logging.error(f"Failed to add torrent: {e}")
            return False
    
    def get_torrents(self) -> List[Dict]:
        """Get all torrents"""
        try:
            response = self.session.get(f"{self.host}/api/v2/torrents/info")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Failed to get torrents: {e}")
            return []
    
    def remove_torrent(self, torrent_hash: str, delete_files: bool = True) -> bool:
        """Remove torrent"""
        try:
            response = self.session.post(
                f"{self.host}/api/v2/torrents/delete",
                data={'hashes': torrent_hash, 'deleteFiles': str(delete_files).lower()}
            )
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Failed to remove torrent: {e}")
            return False

