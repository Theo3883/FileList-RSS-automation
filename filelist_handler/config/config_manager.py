"""Configuration manager with Singleton pattern"""

import yaml
from pathlib import Path


class Config:
    """Singleton configuration manager"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.config_file = Path(__file__).parent.parent.parent / 'config.yml'
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file"""
        if not self.config_file.exists():
            self.create_default_config()
        
        with open(self.config_file, 'r') as f:
            self._config = yaml.safe_load(f)
    
    def create_default_config(self):
        """Create a default configuration file"""
        default_config = {
            'filelist': {
                'rss_url': 'https://filelist.io/rss.php?feed=dl&cat=24,11,29,30,15,18,16,25,6,26,20,2,3,4,19,1,5,10,9,31,17,22,8,28,27,21,23,13,12,7&passkey=69e8a84f711e52ed4e63712d30a85c86',
                'check_interval': 300,
                'max_torrents_per_run': 5,
            },
            'storage': {
                'download_path': '/downloads',
                'max_size_gb': 450,
                'torrents_db': 'torrents.json',
            },
            'torrent_client': {
                'type': 'qbittorrent',
                'host': 'http://localhost:8080',
                'username': 'admin',
                'password': 'adminpass',
            },
            'filters': {
                'freeleech_only': True,
                'min_seeders': 0,
            },
            'logging': {
                'level': 'INFO',
                'file': 'filelist_handler.log',
            }
        }
        
        with open(self.config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        self._config = default_config
    
    def get(self, key: str, default=None):
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    @property
    def rss_feed_url(self) -> str:
        """Get RSS feed URL"""
        return self.get('filelist.rss_url')

