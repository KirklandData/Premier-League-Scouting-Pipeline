import os
import duckdb
import pytest

@pytest.fixture
def db_connection():
    db_path = "data/scouting_vault.duckdb"
    if not os.path.exists(db_path):
        from run_models import build_data_infrastructure
        build_data_infrastructure()
    conn = duckdb.connect(db_path)
    yield conn
    conn.close()

def test_mart_has_rows(db_connection):
    # Verifies database contains clean rows after pipeline runs
    count = db_connection.execute("SELECT COUNT(*) FROM mart_scouting_fixtures").fetchone()
    assert count > 0, "❌ System Alert: Analytical mart contains zero records."

def test_zero_unexpected_nulls(db_connection):
    # Verifies our quality validation constraints successfully caught and patched blank entries
    null_count = db_connection.execute("SELECT COUNT(*) FROM mart_scouting_fixtures WHERE home_score IS NULL OR away_score IS NULL").fetchone()
    assert null_count == 0, "❌ System Alert: Critical missing data leaked into the final database tables."

def test_attendance_cleansing_logic(db_connection):
    # Verifies our COALESCE rule caught missing variables and replaced them with default zeros
    negative_attendance = db_connection.execute("SELECT COUNT(*) FROM mart_scouting_fixtures WHERE clean_attendance < 0").fetchone()
    assert negative_attendance == 0, "❌ System Alert: Invalid formatting anomalies located inside metric parameters."
