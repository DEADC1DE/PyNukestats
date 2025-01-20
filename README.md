# GLFTPD NUKE Statistics

A Python script to process GLFTPD logs, extract NUKE events, store them in a CSV file, and generate user-specific statistics for the past 30 days.

## Features

- **Log Parsing:** Extracts NUKE events from GLFTPD log files using regular expressions.
- **CSV Management:** Stores extracted data in a CSV file, ensuring no duplicate entries and maintaining only the last 30 days of data.
- **User Statistics:** Generates comprehensive statistics for a specified user, including total GB nuked, nuke counts, and detailed event information.
- **Logging:** Provides informative logging to track the script's operations and handle errors.

## Requirements

- Python 3.6 or higher

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/DEADC1DE/PyNukestats.git
   cd nukestats
   nano nukes.py
   Update the following variables in the script to match your environment:
   log_file_path = '/mnt/glftpd/ftp-data/logs/glftpd.log'
   csv_file_path = '/mnt/glftpd/bin/nukes_stats.csv'
   python3 nukes.py update
   ```

## Eggdrop

1. Edit nukes.tcl and put it in eggdrop.conf
2. In IRC !nukestats username 