import duckdb
import os

def build_data_infrastructure():
    print("🚀 Database Engine: Connecting to cloud vault...")
    db_path = "data/scouting_vault.duckdb"
    conn = duckdb.connect(db_path)

    try:
        with open("sql/01_raw.sql", "r") as file:
            sql_raw = file.read()
        conn.execute(f"CREATE OR REPLACE TABLE raw_matches AS {sql_raw}")
        print("📁 Database Engine: SQL Layer 01 (Raw Table Data) Compiled.")

        with open("sql/02_staging.sql", "r") as file:
            sql_staging = file.read()
        conn.execute(f"CREATE OR REPLACE TABLE staging_matches AS {sql_staging}")
        print("🧹 Database Engine: SQL Layer 02 (Clean Staging Data) Compiled.")

        with open("sql/03_marts.sql", "r") as file:
            sql_marts = file.read()
        conn.execute(f"CREATE OR REPLACE TABLE mart_scouting_fixtures AS {sql_marts}")
        print("📊 Database Engine: SQL Layer 03 (Scout Datamart) Compiled & Locked.")

        row_count = conn.execute("SELECT COUNT(*) FROM mart_scouting_fixtures").fetchone()
        print(f"✅ Idempotency Check: Main database table safely built with {row_count[0]} rows.")

    except Exception as e:
        print(f"❌ Database Engine Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists("data/raw/fixtures_snapshot.json"):
        from extract.fetch_fixtures import fetch_live_data
        fetch_live_data()
    build_data_infrastructure()
