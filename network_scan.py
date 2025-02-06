import requests
import time
import os
import hashlib

# Your VirusTotal API Key
API_KEY = "778eacb545422545034de3b9fb71544d337280ae36ac0c94b4a606466c9aeebd"

# VirusTotal API URLs
SCAN_URL = "https://www.virustotal.com/api/v3/urls"
REPORT_URL = "https://www.virustotal.com/api/v3/analyses/{}"
FILE_SCAN_URL = "https://www.virustotal.com/api/v3/files"


def scan_url(url):
    """ Submits a URL to VirusTotal for scanning. """
    headers = {"x-apikey": API_KEY}
    data = {"url": url}

    response = requests.post(SCAN_URL, headers=headers, data=data)

    if response.status_code == 200:
        result = response.json()
        analysis_id = result["data"]["id"]
        print(f"✅ URL submitted successfully! Analysis ID: {analysis_id}")
        return analysis_id
    else:
        print("❌ Failed to submit URL for scanning!")
        return None


def get_scan_results(analysis_id):
    """ Retrieves the scan report from VirusTotal. """
    headers = {"x-apikey": API_KEY}

    # Wait for a few seconds to allow the scan to complete
    time.sleep(10)

    response = requests.get(REPORT_URL.format(analysis_id), headers=headers)

    if response.status_code == 200:
        result = response.json()
        stats = result["data"]["attributes"]["stats"]
        print(f"🔍 Scan Results: {stats}")
    else:
        print("❌ Failed to fetch scan results!")


def scan_file(file_path):
    """ Submits a file for scanning by sending its hash to VirusTotal. """
    headers = {"x-apikey": API_KEY}

    # Get the file hash (MD5)
    file_hash = get_file_hash(file_path)

    if file_hash:
        response = requests.get(f"{FILE_SCAN_URL}/{file_hash}", headers=headers)

        if response.status_code == 200:
            result = response.json()
            stats = result["data"]["attributes"]["last_analysis_stats"]
            print(f"🔍 Scan Results for File: {stats}")
        else:
            print("❌ Failed to scan file!")
    else:
        print("❌ Invalid file!")


def get_file_hash(file_path):
    """ Returns the MD5 hash of a file for scanning. """
    try:
        with open(file_path, "rb") as file:
            file_hash = hashlib.md5()
            while chunk := file.read(8192):  # Read file in chunks
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None


def scan_folder(folder_path):
    """ Scans all files in a folder (by hashing and submitting each file). """
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                print(f"Scanning file: {file_path}")
                scan_file(file_path)
    else:
        print("❌ Folder path is invalid!")


if __name__ == "__main__":
    # Get URL or File/Folder input from the user
    choice = input("Do you want to scan a URL or a file/folder? (Enter 'url' or 'file/folder'): ").strip().lower()

    if choice == 'url':
        url = input("Enter the URL to scan: ").strip()
        analysis_id = scan_url(url)
        if analysis_id:
            get_scan_results(analysis_id)

    elif choice == 'file' or choice == 'folder':
        path = input("Enter the file or folder path: ").strip()
        if os.path.isfile(path):
            scan_file(path)  # Scan a single file
        elif os.path.isdir(path):
            scan_folder(path)  # Scan all files in the folder
        else:
            print("❌ Invalid path! Please check and try again.")
    else:
        print("❌ Invalid choice! Please enter 'url' or 'file/folder'.")