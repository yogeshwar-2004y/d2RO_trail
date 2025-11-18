#!/usr/bin/env python3
"""
Quick script to create iqa_observation_reports table
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database_init import create_iqa_observation_report_table

if __name__ == "__main__":
    print("Creating iqa_observation_reports table...")
    try:
        create_iqa_observation_report_table()
        print("Table created successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

