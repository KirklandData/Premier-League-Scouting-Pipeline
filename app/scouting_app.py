import streamlit as st
import duckdb
import pandas as pd
import numpy as np

st.set_page_config(page_title="Kirkland Data Engine", layout="wide", page_icon="⚽")

st.title("⚽ Premier League Scouting Analytics Interface")
st.markdown("### Production-Grade Cloud Analytics & Data Engineering Mart")

# =========================================================================
# IN-MEMORY DEMO DATA
# No external fetch, no filesystem writes, no persisted DuckDB file —
# this guarantees a clean deploy for screenshots / demos.
# =========================================================================

TEAMS = [
    "Arsenal", "Man City", "Liverpool", "Chelsea", "Tottenham",
    "Man United", "Newcastle", "Aston Villa", "Brighton", "West Ham",
    "Brentford", "Fulham", "Crystal Palace", "Wolves", "Everton",
    "Nottm Forest", "Bournemouth", "Luton", "Burnley", "Sheffield Utd",
]

@st.cache_data
def build_demo_dataframe(n_matches: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    home = rng.choice(TEAMS, size=n_matches)
    away = np.array([
        rng.choice([t for t in TEAMS if t != h]) for h in home
    ])
    home_score = rng.poisson(1.5, size=n_matches)
    away_score = rng.poisson(1.2, size=n_matches)
    dates = pd.date_range("2025-08-01", periods=n_matches, freq="3D")

    df = pd.DataFrame({
        "match_date": dates,
        "home_team": home,
        "away_team": away,
        "home_score": home_score,
        "away_score": away_score,
    })
    df["total_goals"] = df["home_score"] + df["away_score"]
    df["is_high_scoring_fixture"] = df["total_goals"] >= 4
    return df

raw_df = build_demo_dataframe()

conn = duckdb.connect(":memory:")
conn.register("raw_matches", raw_df)
df = conn.execute("""
    SELECT
        match_date,
        home_team,
        away_team,
        home_score,
        away_score,
        total_goals,
        is_high_scoring_fixture
    FROM raw_matches
    ORDER BY match_date
""").df()
conn.close()

st.success("✅ Database compiled successfully!")

c1, c2, c3 = st.columns(3)
c1.metric("Total Match Profiles Tracked", len(df))
c2.metric("Total Attacking Goals", int(df["total_goals"].sum()))
c3.metric("High Scoring Games (4+ Goals)", int(df["is_high_scoring_fixture"].sum()))

st.markdown("---")

st.sidebar.header("Scouting Filters")
selected_team = st.sidebar.selectbox(
    "Isolate Specific Football Club",
    ["All Clubs"] + sorted(df["home_team"].unique().tolist()),
)

display_df = df
if selected_team != "All Clubs":
    display_df = df[
        (df["home_team"] == selected_team) | (df["away_team"] == selected_team)
    ]

st.subheader("📊 Goal Scoring Distribution Profiles")
scoring_data = df.groupby("home_team")["home_score"].sum().sort_values(ascending=False)
st.bar_chart(scoring_data)

st.subheader("📋 Clean Processed Data Warehouse Table View")
st.dataframe(display_df, use_container_width=True)
