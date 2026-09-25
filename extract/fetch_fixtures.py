import os
import json
import random
from datetime import date, timedelta

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TEAMS = [
    "Arsenal", "Man City", "Liverpool", "Chelsea", "Tottenham",
    "Man United", "Newcastle", "Aston Villa", "Brighton", "West Ham",
    "Brentford", "Fulham", "Crystal Palace", "Wolves", "Everton",
    "Nottm Forest", "Bournemouth", "Luton", "Burnley", "Sheffield Utd",
]

def fetch_live_data(n_matches: int = 200, seed: int = 42) -> bool:
    print("📡 Ingestion Station: Generating fixtures snapshot...")
    rng = random.Random(seed)
    start = date(2025, 8, 1)

    fixtures = []
    for i in range(n_matches):
        home = rng.choice(TEAMS)
        away = rng.choice([t for t in TEAMS if t != home])
        fixtures.append({
            "match_id": i + 1,
            "match_date": str(start + timedelta(days=3 * i)),
            "home_team": {"home_team_name": home},
            "away_team": {"away_team_name": away},
            "home_score": rng.randint(0, 4),
            "away_score": rng.randint(0, 3),
            "attendance": rng.randint(18000, 62000),
        })

    try:
        raw_dir = os.path.join(ROOT_DIR, "data", "raw")
        os.makedirs(raw_dir, exist_ok=True)
        out_path = os.path.join(raw_dir, "fixtures_snapshot.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(fixtures, f, indent=4)
        print(f"✅ Ingestion Station: Raw file written to {out_path}")
        return True
    except Exception as e:
        print(f"❌ Ingestion Station Failure: {e}")
        return False

if __name__ == "__main__":
    fetch_live_data()
