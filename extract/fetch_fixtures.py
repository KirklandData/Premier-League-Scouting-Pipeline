import os
import requests
import json

def fetch_live_data():
    print("📡 Ingestion Station: Initialising internet data download...")
    api_url = "https://githubusercontent.com"

    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        payload = response.json()

        os.makedirs("data/raw", exist_ok=True)

        with open("data/raw/fixtures_snapshot.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)
        print("✅ Ingestion Station: Raw file downloaded safely into data/raw/")
        return True
    except Exception as e:
        print(f"❌ Ingestion Station Failure: {e}")
        return False

if __name__ == "__main__":
    fetch_live_data()

