#!/usr/bin/env python3
import re
import csv
import logging
from collections import defaultdict
import sys
from datetime import datetime, timedelta
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

log_file_path = '/mnt/glftpd/ftp-data/logs/glftpd.log'
csv_file_path = '/mnt/glftpd/bin/nukes_stats.csv'

pattern = re.compile(
    r'(?P<timestamp>\w+ \w+ \d+ \d+:\d+:\d+ \d+) NUKE: "(?P<release>.*?)" "(?P<username>.*?)" "(?P<multiplier>\d+)" "(?P<nuke_reason>.*?)" (?P<user_data>.*)'
)

def clean_csv():
    thirty_days_ago = datetime.now() - timedelta(days=30)
    cleaned_entries = []
    if not os.path.exists(csv_file_path):
        return
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                timestamp = datetime.strptime(row['Timestamp'], "%a %b %d %H:%M:%S %Y")
                if timestamp > thirty_days_ago:
                    cleaned_entries.append(row)
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Timestamp', 'Username', 'Release', 'Nuke Reason', 'Multiplier', 'Total GB']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cleaned_entries)
        logging.info(f"Cleaned CSV file. Remaining entries: {len(cleaned_entries)}")
    except Exception as e:
        logging.error(f"Error cleaning CSV file: {e}")


def load_existing_entries():
    existing_keys = set()
    if not os.path.exists(csv_file_path):
        return existing_keys
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                key = (row['Timestamp'], row['Username'], row['Release'], row['Nuke Reason'], row['Multiplier'])
                existing_keys.add(key)
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
    return existing_keys

def save_to_csv(existing_keys):
    new_entries = []
    try:
        with open(log_file_path, 'r', encoding='ISO-8859-1') as file:
            for line in file:
                if len(line.split()) < 6 or line.split()[5] != "NUKE:":
                    continue
                match = pattern.search(line)
                if match:
                    release = match.group('release').split("/")[-1]
                    username = match.group('username')
                    nuke_reason = match.group('nuke_reason')
                    multiplier = match.group('multiplier')
                    kb_values = re.findall(r'(\w+) (\d+\.\d+)', match.group('user_data'))
                    for user, value in kb_values:
                        total_kb = float(value)
                        total_gb = total_kb / 1048576
                        key = (match.group('timestamp'), user, release, nuke_reason, multiplier)
                        if key in existing_keys:
                            continue
                        existing_keys.add(key)
                        new_entries.append({
                            'Timestamp': match.group('timestamp'),
                            'Username': user,
                            'Release': release,
                            'Nuke Reason': nuke_reason,
                            'Multiplier': multiplier,
                            'Total GB': f"{total_gb:.2f}"
                        })
        if not new_entries:
            logging.info("No new NUKE entries found.")
            return
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Timestamp', 'Username', 'Release', 'Nuke Reason', 'Multiplier', 'Total GB']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerows(new_entries)
        logging.info(f"{len(new_entries)} new entries added to the CSV.")
    except Exception as e:
        logging.error(f"Error processing log file: {e}")

def load_user_statistics(username):
    user_statistics = defaultdict(lambda: {
        'total_gb': 0,
        'nuke_reasons': defaultdict(int),
        'count': 0,
        'details': []
    })
    try:
        if os.path.exists(csv_file_path):
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['Username'] == username:
                        total_gb = float(row['Total GB'])
                        user_statistics[username]['total_gb'] += total_gb
                        user_statistics[username]['nuke_reasons'][row['Nuke Reason']] += 1
                        user_statistics[username]['count'] += 1
                        user_statistics[username]['details'].append({
                            'timestamp': row['Timestamp'],
                            'release': row['Release'],
                            'nuke_reason': row['Nuke Reason'],
                            'multiplier': row['Multiplier'],
                            'total_gb': total_gb
                        })
    except Exception as e:
        logging.error(f"Error reading user data from CSV: {e}")
    return user_statistics

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "update":
        clean_csv()
        existing_keys = load_existing_entries()
        save_to_csv(existing_keys)
    elif len(sys.argv) == 2:
        target_username = sys.argv[1]
        statistics = load_user_statistics(target_username)
        if statistics:
            print("\nStatistics for user: " + target_username + " (Last 30 Days)")
            for username, data in statistics.items():
                print(f"\n{'=' * 100}")
                print(f"{'Username':<20} | {'Total GB':<15} | {'Nuke Count':<20}")
                print(f"{'-' * 100}")
                print(f"{username:<20} | {data['total_gb']:<15.2f} GB | {data['count']:<20}")
                print(f"\n{'=' * 100}")
                print(f"{'Timestamp':<25} | {'Release':<60} | {'Nuke Reason':<30} | {'Multiplier':<15} | {'Total GB':<15}")
                print(f"{'-' * 100}")
                for detail in data['details']:
                    print(f"{detail['timestamp']:<25} | {detail['release']:<60} | {detail['nuke_reason']:<30} | {detail['multiplier']:<15} | {detail['total_gb']:<15.2f} GB")
        else:
            print(f"No data found for user: {target_username}.")
    else:
        print("Usage:")
        print("  To update CSV: python3 nukes.py update")
        print("  To get user stats: python3 nukes.py <username>")
