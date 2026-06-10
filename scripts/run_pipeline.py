"""
Bluestock MF Capstone — Master Run Script
Run this to execute the full ETL pipeline end to end.
"""

import subprocess
import sys

scripts = [
    "scripts/data_ingestion.py",
    "scripts/data_cleaning.py",
    "scripts/load_db.py",
]

for script in scripts:
    print(f"\n{'='*50}")
    print(f"Running {script}...")
    print('='*50)
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"ERROR in {script} — stopping.")
        break
    print(f"{script} completed.")

print("\nPipeline complete!")