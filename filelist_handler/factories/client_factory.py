"""Factory for creating torrent clients"""

from ..clients import TorrentClient, QBittorrentClient, TransmissionClient
from ..config import Config


class TorrentClientFactory:
    """Factory for creating torrent clients"""
    
    @staticmethod
    def create_client(config: Config) -> TorrentClient:
        """Create appropriate torrent client based on configuration"""
        client_type = config.get('torrent_client.type', 'qbittorrent')
        host = config.get('torrent_client.host')
        username = config.get('torrent_client.username')
        password = config.get('torrent_client.password')
        
        if client_type == 'qbittorrent':
            return QBittorrentClient(host, username, password)
        elif client_type == 'transmission':
            return TransmissionClient(host, username, password)
        else:
            raise ValueError(f"Unknown torrent client type: {client_type}")

