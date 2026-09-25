import duckdb
import os

def build_data_infrastructure():
    print("🚀 Database Engine: Connecting to local cloud storage vault...")
    
    # Ensure data storage folder exists safely on the server
    os.makedirs("data", exist_ok=True)
    db_path = "data/scouting_vault.duckdb"
    
    # Connect in read-write mode so we have permissions to create the file structure
    conn = duckdb.connect(db_path, read_only=False)
    
    try:
        # Step 1: Compile the Ingestion Layer
        with open("sql/01_raw.sql", "r") as file:
            sql_raw = file.read()
        conn.execute(f"CREATE OR REPLACE TABLE raw_matches AS {sql_raw}")
        print("📁 SQL Layer 01 (Raw Table Data) Compiled.")
        
        # Step 2: Compile the Cleaning Layer
        with open("sql/02_staging.sql", "r") as file:
            sql_staging = file.read()
        conn.execute(f"CREATE OR REPLACE TABLE staging_matches AS {sql_staging}")
        print("扫 SQL Layer 02 (Clean Staging Data) Compiled.")
        
        # Step 3: Compile the Final Summary Layer
        with open("sql/03_marts.sql", "r") as file:
            sql_marts = file.read()
        conn.execute(f"CREATE OR REPLACE TABLE mart_scouting_fixtures AS {sql_marts}")
        print("📊 SQL Layer 03 (Scout Datamart Data) Compiled and Locked.")
        
    except Exception as e:
        print(f"❌ Database Compiling Error: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists("data/raw/fixtures_snapshot.json"):
        from extract.fetch_fixtures import fetch_live_data
        fetch_live_data()
    build_data_infrastructure()
