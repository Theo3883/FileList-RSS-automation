# FileList Handler - Service Management

The FileList RSS Handler is configured as an OpenRC service for Alpine Linux.

## Service Management

### Start the service
```bash
rc-service filelist-handler start
```

### Stop the service
```bash
rc-service filelist-handler stop
```

### Restart the service
```bash
rc-service filelist-handler restart
```

### Check status
```bash
rc-service filelist-handler status
```

### Enable on boot
```bash
rc-update add filelist-handler default
```

### Disable on boot
```bash
rc-update del filelist-handler default
```

### View boot services
```bash
rc-update show
```

## How It Works

### Service Dependencies

The service is configured to:
- ✅ **Depend on** `qbittorrent-nox` service
- ✅ **Start after** qBittorrent is running
- ✅ **Wait up to 60 seconds** for qBittorrent to be ready
- ✅ **Retry connection** if qBittorrent isn't ready yet

### Retry Logic

**Two levels of retry protection:**

1. **OpenRC init script** (service level):
   - Waits for qBittorrent service to be running
   - Checks if Web UI is responding
   - Waits up to 60 seconds (30 attempts × 2 seconds)

2. **Python handler** (application level):
   - Additional retry logic built into the handler
   - Will retry connection up to 30 times (60 seconds)
   - Logs retry attempts

### Service File Location

- **Init script**: `/etc/init.d/filelist-handler`
- **Source**: `/root/scripts/filelist-handler.init`
- **PID file**: `/var/run/filelist-handler.pid`
- **Logs**: `/root/scripts/filelist_handler.log`

## Service Configuration

The service file (`/etc/init.d/filelist-handler`) defines:

```bash
# Dependencies
depend() {
    need qbittorrent-nox    # Requires qBittorrent
    after qbittorrent-nox   # Start after qBittorrent
    use net                 # Need network
}
```

## Testing

### Test service start
```bash
rc-service filelist-handler start
rc-service filelist-handler status
tail -f /root/scripts/filelist_handler.log
```

### Test boot sequence
```bash
# Reboot to test
reboot

# After reboot, check if both services started
rc-service qbittorrent-nox status
rc-service filelist-handler status
```

### Manual start (for testing)
```bash
# Stop service
rc-service filelist-handler stop

# Start manually to see output
/usr/bin/python3 /root/scripts/run.py
```

## Troubleshooting

### Service won't start

```bash
# Check qBittorrent is running
rc-service qbittorrent-nox status

# Check logs
tail -50 /root/scripts/filelist_handler.log

# Check service dependencies
rc-status -a | grep filelist
```

### Service starts but fails

```bash
# Check if handler can connect
python3 /root/scripts/test_connection.py

# Check qBittorrent Web UI
curl -u admin:ADMINADMIN http://localhost:8080/api/v2/app/version
```

### Service not starting on boot

```bash
# Verify it's enabled
rc-update show | grep filelist

# Check boot log
dmesg | grep filelist

# Check service log
cat /var/log/messages | grep filelist
```

### Remove service (if needed)

```bash
# Stop service
rc-service filelist-handler stop

# Remove from boot
rc-update del filelist-handler

# Remove init script
rm /etc/init.d/filelist-handler
```

## Service Commands Summary

| Command | Description |
|---------|-------------|
| `rc-service filelist-handler start` | Start the service |
| `rc-service filelist-handler stop` | Stop the service |
| `rc-service filelist-handler restart` | Restart the service |
| `rc-service filelist-handler status` | Check if running |
| `rc-update add filelist-handler default` | Enable on boot |
| `rc-update del filelist-handler default` | Disable on boot |
| `rc-update show` | List all boot services |

## Alternative: Using the helper scripts

You can still use the helper scripts even with the service:

```bash
# Helper scripts work with service too
./start.sh
./stop.sh
./status.sh
```

However, the **OpenRC service is recommended** for production use as it:
- ✅ Starts automatically on boot
- ✅ Properly handles dependencies
- ✅ Integrates with system service management
- ✅ Provides better logging and monitoring

