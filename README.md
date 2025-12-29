# FileList Torrent RSS Handler

A professional, object-oriented Python application for automatically managing FileList torrents via RSS feeds with intelligent storage management.

## 🎯 Key Features

- ✅ **Automatic Downloads**: Downloads 5 freeleech torrents per run automatically
- ✅ **OOP Design**: Clean, maintainable code using multiple design patterns
- ✅ **Modular Architecture**: Separated into logical modules for easy maintenance
- ✅ **Smart Storage Management**: Automatically deletes oldest torrents when storage exceeds 450GB
- ✅ **Freeleech-Only Filtering**: Only downloads freeleech torrents to protect your ratio
- ✅ **Service Management**: Runs as OpenRC service with automatic startup
- ✅ **Retry Logic**: Automatically retries if qBittorrent isn't ready

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /root/scripts
apk add py3-yaml py3-requests py3-feedparser
```

### 2. Start qBittorrent-nox

```bash
rc-service qbittorrent-nox start
```

### 3. Test Connection

```bash
python3 test_connection.py
```

### 4. Start the Handler

#### Option A: As a Service (Recommended)

```bash
# Start service
rc-service filelist-handler start

# Enable on boot
rc-update add filelist-handler default

# Check status
rc-service filelist-handler status
```

#### Option B: Manual Start

```bash
./start.sh
```

## 📦 Project Structure

```
/root/scripts/
├── filelist_handler/          # Main application package
│   ├── main.py               # Main orchestration logic
│   ├── config/               # Configuration management
│   ├── models/               # Data models
│   ├── clients/              # Torrent clients
│   ├── parsers/              # RSS parser
│   ├── storage/              # Storage management
│   ├── observers/            # Event system
│   └── factories/            # Client factory
├── run.py                    # Entry point
├── config.yml               # Configuration
├── filelist-handler.init    # OpenRC service script
└── SERVICE.md               # Service management guide
```

## ⚙️ Configuration

Edit `config.yml` to customize:

```yaml
filelist:
  rss_url: 'https://filelist.io/rss.php?...'
  max_torrents_per_run: 5      # Torrents per check
  check_interval: 300          # Check every 5 minutes

storage:
  download_path: '/downloads'
  max_size_gb: 450            # Storage limit

torrent_client:
  type: 'qbittorrent'
  host: 'http://localhost:8080'
  username: 'admin'
  password: 'ADMINADMIN'
```

## 🔧 Service Management

The handler runs as an OpenRC service with automatic dependency handling:

```bash
# Service commands
rc-service filelist-handler start
rc-service filelist-handler stop
rc-service filelist-handler restart
rc-service filelist-handler status

# Enable on boot
rc-update add filelist-handler default

# View all services
rc-update show
```

**See `SERVICE.md` for complete service documentation.**

## 📊 How It Works

### Every 5 Minutes:

1. **Fetch RSS Feed** from FileList
2. **Find Freeleech Torrents** (only `[FreeLeech]` tagged)
3. **Download up to 5** new torrents
4. **Check Storage** before each download
5. **Auto-cleanup** if storage > 450GB (deletes oldest)
6. **Add to qBittorrent-nox** automatically
7. **Save to Database** (torrents.json)
8. **Log Everything** to filelist_handler.log
9. **Sleep 5 minutes** and repeat

## 🔒 Retry Logic

### Two-Level Protection:

1. **Service Level** (OpenRC init script):
   - Waits for qBittorrent service to start
   - Checks if Web UI is responding
   - Waits up to 60 seconds

2. **Application Level** (Python handler):
   - Retries connection up to 30 times
   - Logs each retry attempt
   - Gracefully handles failures

## 📝 Monitoring

### View Logs

```bash
# Real-time logs
tail -f filelist_handler.log

# Last 50 lines
tail -50 filelist_handler.log
```

### Check Status

```bash
# Service status
rc-service filelist-handler status

# Process status
ps aux | grep run.py

# Database
cat torrents.json | python3 -m json.tool
```

## 🛠️ Troubleshooting

### Service won't start

```bash
# Check qBittorrent is running
rc-service qbittorrent-nox status

# Check logs
tail -50 filelist_handler.log

# Test connection manually
python3 test_connection.py
```

### No torrents downloading

```bash
# Check logs for errors
grep ERROR filelist_handler.log

# Verify RSS feed
curl -s "YOUR_RSS_URL" | head -20

# Check qBittorrent
curl -u admin:ADMINADMIN http://localhost:8080/api/v2/torrents/info
```

## 📚 Documentation

- **SERVICE.md** - Complete service management guide
- **config.yml** - Configuration with comments
- **filelist_handler/** - Source code (well-documented)

## 🎨 Design Patterns

- **Singleton**: Configuration management
- **Strategy**: Multiple torrent client support
- **Factory**: Client instantiation
- **Observer**: Event notification system
- **Repository**: Data persistence

## 🔒 Safety Features

- ✅ Only downloads freeleech (protects ratio)
- ✅ Never exceeds storage limit
- ✅ Prevents duplicate downloads
- ✅ Smart cleanup (deletes oldest first)
- ✅ Complete audit trail in logs

## 📈 Features

- ✅ Automatic operation (no manual intervention)
- ✅ Smart storage management
- ✅ Service integration (OpenRC)
- ✅ Dependency handling (waits for qBittorrent)
- ✅ Retry logic (handles failures gracefully)
- ✅ Comprehensive logging
- ✅ Production-ready code

## 💡 Tips

1. **Monitor logs** regularly for the first few runs
2. **Check storage** to ensure enough space
3. **Adjust limits** in config.yml if needed
4. **Use service** for production (not manual start)
5. **Keep freeleech_only: true** to protect ratio

---

**Enjoy automated freeleech torrent management!** 🎉
