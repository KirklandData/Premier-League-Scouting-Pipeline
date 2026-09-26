import os
import requests

# Real, genuine Premier League match data — no invented figures, no synthetic
# generator. Source: football-data.co.uk, a long-standing free, open, no-API-key
# archive of official match results used widely in football analytics.
#
# We use the 2024/25 season deliberately: the last FULLY COMPLETED Premier
# League season before 2025/26, so every result in this pipeline is a real,
# verifiable match that actually happened.
SEASON_CODE = "2425"   # 2024/25 season
DIVISION_CODE = "E0"   # E0 = English Premier League (top flight)
SOURCE_URL = f"https://www.football-data.co.uk/mmz4281/{SEASON_CODE}/{DIVISION_CODE}.csv"

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_PATH = os.path.join(ROOT_DIR, "data", "raw", "fixtures_snapshot.csv")


def fetch_live_data() -> bool:
    print(f"📡 Ingestion Station: Downloading real 2024/25 Premier League results from {SOURCE_URL}")
    try:
        response = requests.get(SOURCE_URL, timeout=20)
        response.raise_for_status()

        # Sanity check — a genuine season file is comfortably larger than a
        # few KB; anything tiny suggests we got an error page, not real data
        if len(response.content) < 5_000:
            raise ValueError(
                f"Downloaded file is suspiciously small ({len(response.content)} bytes) — "
                "likely an error page rather than real match data."
            )

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

        # Saved exactly as downloaded — no reshaping, no reformatting.
        # This IS the raw layer: an untouched copy of the real source file.
        with open(OUTPUT_PATH, "wb") as f:
            f.write(response.content)

        print(f"✅ Ingestion Station: Real season data saved to {OUTPUT_PATH} ({len(response.content):,} bytes)")
        return True

    except Exception as e:
        print(f"❌ Ingestion Station Failure: {e}")
        return False


if __name__ == "__main__":
    fetch_live_data()
