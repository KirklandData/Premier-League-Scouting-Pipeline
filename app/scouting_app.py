import streamlit as st
import duckdb
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from run_models import build_data_infrastructure

st.set_page_config(page_title="Premier League Scouting Analytics", layout="wide", page_icon="⚽")

st.title("⚽ Premier League Scouting Analytics Interface")
st.markdown("### Real 2024/25 Season Data — Cloud Analytics & Data Engineering Mart")

db_path = os.path.join(ROOT_DIR, "data", "scouting_vault.duckdb")

if not os.path.exists(db_path):
    with st.spinner("First-time setup: downloading real season data and building the database..."):
        build_data_infrastructure()

conn = duckdb.connect(db_path, read_only=True)
df = conn.execute("SELECT * FROM mart_scouting_fixtures ORDER BY match_date").df()
conn.close()

st.success(f"✅ Loaded {len(df)} real Premier League matches from the 2024/25 season.")

c1, c2, c3 = st.columns(3)
c1.metric("Total Matches Tracked", len(df))
c2.metric("Total Goals Scored", int(df["home_score"].sum() + df["away_score"].sum()))
c3.metric("High-Scoring Games (4+ Goals)", int(df["is_high_scoring_fixture"].sum()))

st.markdown("---")

st.sidebar.header("Scouting Filters")
all_teams = sorted(set(df["home_team"]).union(set(df["away_team"])))
selected_team = st.sidebar.selectbox("Isolate Specific Football Club", ["All Clubs"] + all_teams)

display_df = df
if selected_team != "All Clubs":
    display_df = df[(df["home_team"] == selected_team) | (df["away_team"] == selected_team)]

st.subheader("📊 Total Goals Scored by Club (Home + Away)")
home_goals = df.groupby("home_team")["home_score"].sum()
away_goals = df.groupby("away_team")["away_score"].sum()
scoring_data = home_goals.add(away_goals, fill_value=0).sort_values(ascending=False)
st.bar_chart(scoring_data)

st.subheader("📋 Clean Processed Data Warehouse Table View")
display_df = display_df.copy()
display_df["match_date"] = display_df["match_date"].dt.strftime("%Y-%m-%d")
st.dataframe(display_df, use_container_width=True)
