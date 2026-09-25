import os
import json

def fetch_live_data():
    print("📡 Ingestion Station: Generating secure match day snapshots...")
    
    # Immutable raw football scouting dataset grid
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
    
    try:
        # Create storage directories safely on the cloud server
        os.makedirs("data/raw", exist_ok=True)
        
        # Commit the snapshot file to disk path
        output_path = "data/raw/fixtures_snapshot.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(mock_matches, f, indent=4)
            
        print(f"✅ Ingestion Station: Raw dataset successfully anchored to {output_path}")
        return True
    except Exception as e:
        print(f"❌ Ingestion Station Failure: {e}")
        return False

if __name__ == "__main__":
    fetch_live_data()
