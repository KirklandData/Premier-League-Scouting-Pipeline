import duckdb
import os
import sys

def build_data_infrastructure():
    print("🚀 Initialising DuckDB Core Modeller...")
    
    # Resolve directory paths relative to this script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    sql_dir = os.path.join(base_dir, "sql")
    db_path = os.path.join(data_dir, "scouting_vault.duckdb")
    
    os.makedirs(data_dir, exist_ok=True)
    
    # Force a clean slate by deleting any stale or locked database file
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("💥 Stale database file successfully cleared.")
        except Exception:
            pass
            
    # Establish a fresh connection in write-mode to compile the schemas
    conn = duckdb.connect(db_path, read_only=False)
    
    try:
        # Drop existing tables to break open cached structures completely
        conn.execute("DROP TABLE IF EXISTS mart_scouting_fixtures;")
        conn.execute("DROP TABLE IF EXISTS staging_matches;")
        conn.execute("DROP TABLE IF EXISTS raw_matches;")
        
        # Step 1: Compile the Raw Ingestion Layer
        with open(os.path.join(sql_dir, "01_raw.sql"), "r") as file:
            sql_raw = file.read()
        conn.execute(f"CREATE TABLE raw_matches AS {sql_raw}")
        print("📁 SQL Layer 01 (Raw Table Data) Compiled.")
        
        # Step 2: Compile the Staging Cleansing Layer
        with open(os.path.join(sql_dir, "02_staging.sql"), "r") as file:
            sql_staging = file.read()
        conn.execute(f"CREATE TABLE staging_matches AS {sql_staging}")
        print("🧹 SQL Layer 02 (Clean Staging Data) Compiled.")
        
        # Step 3: Compile the Final Datamart Layer
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
    from extract.fetch_fixtures import fetch_live_data
    fetch_live_data()
    build_data_infrastructure()
