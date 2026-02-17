# Requirements:
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os
import csv
import argparse
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
SERVICE_ACCOUNT_FILE = '/HERE IS THE FILE PATH TO YOUR JSON KEY FILE' # Path to your JSON key file
SPREADSHEET_ID = 'YOUR SPREAD SHEET ID'
#https://docs.google.com/spreadsheets/d/SPEADSHEET_ID/edit?gid=0#gid=0
# use only the ID in the SPREADSHEET_ID portion

def upload_csv_to_sheet(csv_filename, range_name, skip_header=False):
    """
    Reads a local CSV file and uploads it to Google Sheets.
    """
    # 1. Authenticate
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found.")
        return

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])

    service = build('sheets', 'v4', credentials=creds)

    # 2. Prepare Data
    values = []
    try:
        with open(csv_filename, 'r', encoding='utf-16') as f:
            reader = csv.reader(f)
            if skip_header:
                next(reader, None)  # Skip the header row
            values = list(reader)
    except FileNotFoundError:
        print(f"Error: {csv_filename} not found.")
        return

    if not values:
        print(f"Skipping empty file (or file with only header): {csv_filename}")
        return

    body = {
        'values': values
    }

    # 3. Execute Upload
    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, 
            range=range_name,
            valueInputOption='USER_ENTERED', 
            insertDataOption='INSERT_ROWS',
            body=body).execute()
        
        print(f"Appended {os.path.basename(csv_filename)} to {range_name}: {result.get('updates').get('updatedCells')} cells updated.")
    except Exception as e:
        print(f"An error occurred uploading {csv_filename}: {e}")

def upload_all_csvs_in_folder(folder_path, sheet_name, delay=1):
    """
    Iterates through all CSV files in a folder and appends them to a single sheet.
    Only the first file's header is uploaded.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a directory.")
        return

    range_name = f"'{sheet_name}'!A1"
    first_file = True
    
    # Sort files to ensure consistent order
    files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.csv')])
    
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        
        # Only keep header for the very first file
        skip_header = not first_file
        
        upload_csv_to_sheet(file_path, range_name, skip_header=skip_header)
        
        first_file = False
        
        if delay > 0:
            print(f"Waiting {delay} seconds before next upload...")
            time.sleep(delay)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload CSV files from a folder to Google Sheets.')
    parser.add_argument('--folder', '-f', type=str, default='reports',
                        help='Path to the folder containing CSV files (default: reports)')
    parser.add_argument('--sheet', '-s', type=str, default='Sheet1',
                        help='Name of the existing sheet to upload data to (default: Sheet1)')
    parser.add_argument('--delay', '-d', type=float, default=1.0,
                        help='Delay in seconds between uploads to avoid rate limits (default: 1.0)')
    
    args = parser.parse_args()
    
    upload_all_csvs_in_folder(args.folder, args.sheet, args.delay)
