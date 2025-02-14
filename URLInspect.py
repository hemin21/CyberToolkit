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


def select_file_from_folder(folder_path):
    """ Allows the user to select a specific file from a folder for scanning. """
    if not os.path.isdir(folder_path):
        print("❌ Invalid folder path!")
        return None

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not files:
        print("❌ No files found in the folder!")
        return None

    print("\n📂 Files in folder:")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

    try:
        choice = int(input("\nEnter the number of the file you want to scan: "))
        if 1 <= choice <= len(files):
            return os.path.join(folder_path, files[choice - 1])
        else:
            print("❌ Invalid choice!")
            return None
    except ValueError:
        print("❌ Please enter a valid number!")
        return None


if __name__ == "__main__":
    choice = input("Do you want to scan a URL or a file/folder? (Enter 'url' or 'file/folder'): ").strip().lower()

    if choice == 'url':
        url = input("Enter the URL to scan: ").strip()
        analysis_id = scan_url(url)
        if analysis_id:
            get_scan_results(analysis_id)

    elif choice == 'file':
        file_path = input("Enter the full file path to scan: ").strip()
        if os.path.isfile(file_path):
            scan_file(file_path)
        else:
            print("❌ Invalid file path!")

    elif choice == 'folder':
        folder_path = input("Enter the folder path: ").strip()
        file_path = select_file_from_folder(folder_path)
        if file_path:
            scan_file(file_path)
    else:
        print("❌ Invalid choice! Please enter 'url' or 'file/folder'.")
