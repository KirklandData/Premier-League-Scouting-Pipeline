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
    count = db_connection.execute("SELECT COUNT(*) FROM mart_scouting_fixtures").fetchone()
    assert count[0] > 0, "❌ Quality Error: Database data mart contains zero records."

def test_zero_unexpected_nulls(db_connection):
    null_count = db_connection.execute("SELECT COUNT(*) FROM mart_scouting_fixtures WHERE home_score IS NULL OR away_score IS NULL").fetchone()
    assert null_count[0] == 0, "❌ Quality Error: Broken empty score fields leaked into our system."

def test_attendance_cleansing_logic(db_connection):
    negative_attendance = db_connection.execute("SELECT COUNT(*) FROM mart_scouting_fixtures WHERE clean_attendance < 0").fetchone()
    assert negative_attendance[0] == 0, "❌ Quality Error: Invalid negative text parameters located in database columns."
