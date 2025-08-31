# GLFTPD NUKE Statistics

A Python script to process GLFTPD logs, extract NUKE events, store them in a CSV file, and generate user-specific statistics for the past 30 days.

## Features

- **Log Parsing:** Extracts NUKE events from GLFTPD log files using regular expressions
- **CSV Management:** Stores extracted data in a CSV file, ensuring no duplicate entries and maintaining only the last 30 days of data
- **User Statistics:** Generates comprehensive statistics for a specified user, including total GB nuked, nuke counts, and detailed event information
- **IRC Integration:** Real-time statistics via Eggdrop bot commands
- **Logging:** Provides informative logging to track the script's operations and handle errors

## Requirements

- Python 3.6 or higher
- GLFTPD server with standard log format
- Eggdrop bot (for IRC integration)

## Installation

1. **Configure paths in nukes.py:**
   ```python
   log_file_path = '/mnt/glftpd/ftp-data/logs/glftpd.log'
   csv_file_path = '/mnt/glftpd/bin/Ottostats/nukes_stats.csv'
   ```

2. **Set up crontab for automatic updates:**
   ```bash
   crontab -e
   # Add this line:
   59 23 * * *     /mnt/glftpd/bin/pyNukestats/nukes.py update
   ```

3. **Set file permissions:**
   ```bash
   chmod +x nukes.py
   ```

## Usage

```bash
# Update CSV database from logs
python3 nukes.py update

# Get statistics for specific user
python3 nukes.py username
```

## Eggdrop Integration

1. Add `stats.tcl` to your eggdrop configuration:
   ```tcl
   source scripts/stats.tcl
   ```

2. IRC Commands:
   ```
   !nukestats              # Show your own statistics
   !nukestats username     # Show statistics for specific user
   ```

## File Structure

- `nukes.py` - Main Python script
- `stats.tcl` - Eggdrop integration script  
- `nukes_stats.csv` - CSV database (auto-created)

## Output Format

The script generates colorized IRC output showing:
- Total GB nuked and credit losses
- Detailed nuke history with timestamps
- Top nuke reasons
- Multiplier calculations