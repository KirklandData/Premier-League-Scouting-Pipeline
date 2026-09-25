import os
import json
import random
from datetime import date, timedelta

TEAMS = [
    "Arsenal", "Man City", "Liverpool", "Chelsea", "Tottenham",
    "Man United", "Newcastle", "Aston Villa", "Brighton", "West Ham",
    "Brentford", "Fulham", "Crystal Palace", "Wolves", "Everton",
    "Nottm Forest", "Bournemouth", "Luton", "Burnley", "Sheffield Utd",
]

def fetch_live_data(n_generated: int = 100, seed: int = 42) -> bool:
    print("📡 Ingestion Station: Generating secure match day snapshots...")

    # Deliberate anomaly rows — kept as-is to prove the staging layer's
    # COALESCE (attendance) and WHERE (missing score) logic actually works
    mock_matches = [
        {
            "match_id": 1,
            "match_date": "2026-09-12",
            "home_team": {"home_team_name": "Arsenal"},
            "away_team": {"away_team_name": "Chelsea"},
            "home_score": 3,
            "away_score": 1,
            "attendance": 60231
        },
        {
            "match_id": 2,
            "match_date": "2026-09-13",
            "home_team": {"home_team_name": "Liverpool"},
            "away_team": {"away_team_name": "Everton"},
            "home_score": 2,
            "away_score": 0,
            "attendance": 54022
        },
        {
            "match_id": 3,
            "match_date": "2026-09-14",
            "home_team": {"home_team_name": "Brighton"},
            "away_team": {"away_team_name": "Ipswich"},
            "home_score": 1,
            "away_score": 1,
            "attendance": None  # Minor blank anomaly to test our COALESCE logic gate
        },
        {
            "match_id": 4,
            "match_date": "2026-09-14",
            "home_team": {"home_team_name": "Tottenham"},
            "away_team": {"away_team_name": "Brentford"},
            "home_score": None,  # Critical blank anomaly to test our WHERE sanitation filter
            "away_score": 2,
            "attendance": 58100
        }
    ]

    # Bulk-generate additional realistic rows on top of the anomaly set
    rng = random.Random(seed)
    start_date = date(2026, 9, 15)
    next_id = len(mock_matches) + 1

    for i in range(n_generated):
        home = rng.choice(TEAMS)
        away = rng.choice([t for t in TEAMS if t != home])
        mock_matches.append({
            "match_id": next_id + i,
            "match_date": str(start_date + timedelta(days=i)),
            "home_team": {"home_team_name": home},
            "away_team": {"away_team_name": away},
            "home_score": rng.randint(0, 4),
            "away_score": rng.randint(0, 3),
            "attendance": rng.randint(18000, 62000),
        })

    try:
        os.makedirs("data/raw", exist_ok=True)
        output_path = "data/raw/fixtures_snapshot.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(mock_matches, f, indent=4)

        print(f"✅ Ingestion Station: Raw dataset successfully anchored to {output_path} ({len(mock_matches)} rows)")
        return True
    except Exception as e:
        print(f"❌ Ingestion Station Failure: {e}")
        return False

if __name__ == "__main__":
    fetch_live_data()
