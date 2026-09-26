import os
import sys
import duckdb
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from run_models import build_data_infrastructure

DB_PATH = os.path.join(ROOT_DIR, "data", "scouting_vault.duckdb")


@pytest.fixture(scope="module", autouse=True)
def build_pipeline():
    build_data_infrastructure()
    yield


def get_connection():
    return duckdb.connect(DB_PATH, read_only=True)


def test_mart_table_is_not_empty():
    conn = get_connection()
    row_count = conn.execute("SELECT COUNT(*) FROM mart_scouting_fixtures").fetchone()[0]
    conn.close()
    assert row_count > 0, "The final datamart should contain at least one match."


def test_no_null_scores_in_final_mart():
    conn = get_connection()
    null_count = conn.execute("""
        SELECT COUNT(*) FROM mart_scouting_fixtures
        WHERE home_score IS NULL OR away_score IS NULL
    """).fetchone()[0]
    conn.close()
    assert null_count == 0, "No match in the final mart should be missing a score."


def test_no_duplicate_matches():
    conn = get_connection()
    duplicates = conn.execute("""
        SELECT match_id, COUNT(*) AS c
        FROM mart_scouting_fixtures
        GROUP BY match_id
        HAVING COUNT(*) > 1
    """).fetchall()
    conn.close()
    assert len(duplicates) == 0, "Every match_id should appear exactly once."


def test_total_goals_is_non_negative():
    conn = get_connection()
    min_goals = conn.execute("SELECT MIN(total_goals) FROM mart_scouting_fixtures").fetchone()[0]
    conn.close()
    assert min_goals >= 0, "Total goals per match should never be negative."
