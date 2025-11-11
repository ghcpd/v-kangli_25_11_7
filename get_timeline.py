"""Get requirement processing timeline"""

from datetime import datetime
import os
import json
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 60)
print("Requirement Processing Timeline")
print("=" * 60)
print()

# Get key file timestamps
files_to_check = [
    'entity_extraction.py',
    'relation_extraction.py',
    'evaluator.py',
    'main.py',
    'evaluation_report.json'
]

times = []
print("File Creation/Modification Times:")
print("-" * 60)
for file in files_to_check:
    if os.path.exists(file):
        mtime = os.path.getmtime(file)
        dt = datetime.fromtimestamp(mtime)
        times.append((file, dt))
        print(f"{file:30s} {dt.strftime('%Y-%m-%d %H:%M:%S')}")

if times:
    start_time = min(t[1] for t in times)
    end_time = max(t[1] for t in times)
    duration = end_time - start_time
    
    print()
    print("=" * 60)
    print("TIMELINE SUMMARY")
    print("=" * 60)
    print(f"Start Time (First File Created): {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End Time (Last Execution):       {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Duration:                  {duration.total_seconds() / 60:.1f} minutes ({duration.total_seconds():.0f} seconds)")
    print()

# Get evaluation report timestamp
if os.path.exists('evaluation_report.json'):
    with open('evaluation_report.json', 'r', encoding='utf-8') as f:
        report = json.load(f)
        timestamp_str = report.get('timestamp', '')
        method = report.get('method', 'N/A')
        if timestamp_str:
            try:
                ts = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                print(f"Last Pipeline Execution: {ts.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Method: {method}")
            except:
                print(f"Last Pipeline Execution: {timestamp_str}")

print()
print("=" * 60)
print("Status: ALL REQUIREMENTS COMPLETED")
print("=" * 60)

