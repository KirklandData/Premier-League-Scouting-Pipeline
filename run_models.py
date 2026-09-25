import duckdb
import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def build_data_infrastructure():
    print("🚀 Database Engine: Connecting to local cloud storage vault...")

    os.chdir(ROOT_DIR)  # guarantees relative SQL paths (e.g. in 01_raw.sql) always resolve correctly

    data_dir = os.path.join(ROOT_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "scouting_vault.duckdb")
    sql_dir = os.path.join(ROOT_DIR, "sql")

    conn = duckdb.connect(db_path, read_only=False)

    try:
        with open(os.path.join(sql_dir, "01_raw.sql"), "r") as file:
            sql_raw = file.read()
        conn.execute(f"CREATE OR REPLACE TABLE raw_matches AS {sql_raw}")
        print("📁 SQL Layer 01 (Raw Table Data) Compiled.")

        with open(os.path.join(sql_dir, "02_staging.sql"), "r") as file:
            sql_staging = file.read()
        conn.execute(f"CREATE OR REPLACE TABLE staging_matches AS {sql_staging}")
        print("🧹 SQL Layer 02 (Clean Staging Data) Compiled.")

        with open(os.path.join(sql_dir, "03_marts.sql"), "r") as file:
            sql_marts = file.read()
        conn.execute(f"CREATE OR REPLACE TABLE mart_scouting_fixtures AS {sql_marts}")
        print("📊 SQL Layer 03 (Scout Datamart Data) Compiled and Locked.")

    except Exception as e:
        print(f"❌ Database Compiling Error: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    raw_json_path = os.path.join(ROOT_DIR, "data", "raw", "fixtures_snapshot.json")
    if not os.path.exists(raw_json_path):
        from extract.fetch_fixtures import fetch_live_data
        success = fetch_live_data()
        if not success:
            raise RuntimeError("Fixture ingestion failed — cannot proceed to build.")
    build_data_infrastructure()
