import duckdb
import os
from extract.fetch_fixtures import fetch_live_data

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def build_data_infrastructure():
    print("🚀 Initialising DuckDB Core Modeller...")

    os.chdir(ROOT_DIR)

    raw_csv_path = os.path.join(ROOT_DIR, "data", "raw", "fixtures_snapshot.csv")
    if not os.path.exists(raw_csv_path):
        print("📡 Raw fixtures snapshot missing — downloading real season data now...")
        success = fetch_live_data()
        if not success:
            raise RuntimeError("Fixture ingestion failed — cannot proceed to build.")

    data_dir = os.path.join(ROOT_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "scouting_vault.duckdb")

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = duckdb.connect(db_path, read_only=False)

    try:
        sql_dir = os.path.join(ROOT_DIR, "sql")

        with open(os.path.join(sql_dir, "01_raw.sql"), "r") as file:
            sql_raw = file.read()
        conn.execute(f"CREATE TABLE raw_matches AS {sql_raw}")
        print("📁 SQL Layer 01 (Raw Table Data) Compiled.")

        with open(os.path.join(sql_dir, "02_staging.sql"), "r") as file:
            sql_staging = file.read()
        conn.execute(f"CREATE TABLE staging_matches AS {sql_staging}")
        print("🧹 SQL Layer 02 (Clean Staging Data) Compiled.")

        with open(os.path.join(sql_dir, "03_marts.sql"), "r") as file:
            sql_marts = file.read()
        conn.execute(f"CREATE TABLE mart_scouting_fixtures AS {sql_marts}")
        print("📊 SQL Layer 03 (Scout Datamart) Locked.")

    except Exception as e:
        print(f"❌ Critical Pipeline Failure: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    build_data_infrastructure()
