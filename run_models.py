import duckdb
import os

def build_data_infrastructure():
    print("🚀 Initialising DuckDB Core Modeller...")
    
    # Force creation of target data path
    os.makedirs("data", exist_ok=True)
    db_path = "data/scouting_vault.duckdb"
    
    # Establish a fresh, clean write-mode connection
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = duckdb.connect(db_path, read_only=False)
    
    try:
        # Step 1: Run Raw Grid Parsing
        with open("sql/01_raw.sql", "r") as file:
            sql_raw = file.read()
        conn.execute(f"CREATE TABLE raw_matches AS {sql_raw}")
        print("📁 SQL Layer 01 (Raw Table Data) Compiled.")
        
        # Step 2: Run Cleansing Filters
        with open("sql/02_staging.sql", "r") as file:
            sql_staging = file.read()
        conn.execute(f"CREATE TABLE staging_matches AS {sql_staging}")
        print("🧹 SQL Layer 02 (Clean Staging Data) Compiled.")
        
        # Step 3: Run Scout Analytics Datamart
        with open("sql/03_marts.sql", "r") as file:
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
