import streamlit as st
import duckdb
import pandas as pd
import os
import sys

# Dynamic root directory resolution
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

st.set_page_config(page_title="Kirkland Data Engine", layout="wide")

st.title("⚽ Premier League Scouting Analytics Interface")
st.markdown("### Production-Grade Cloud Analytics & Data Engineering Mart")

db_path = os.path.join(base_dir, "data", "scouting_vault.duckdb")

# Run models automatically to generate the database asset if missing on cloud boot
if not os.path.exists(db_path):
    with st.spinner("📦 First-time deployment detected. Initialising DuckDB SQL schemas..."):
        from run_models import build_data_infrastructure
        build_data_infrastructure()
    st.success("✅ Database structures successfully built!")

try:
    # Read the final analytical dataset mart table
    conn = duckdb.connect(db_path, read_only=True)
    df = conn.execute("SELECT * FROM mart_scouting_fixtures").df()
    conn.close()
    
    # High-Level Summary Metric Cards
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Match Profiles Tracked", len(df))
    c2.metric("Total Attacking Goals", int(df["total_goals"].sum()))
    c3.metric("High Scoring Games (4+ Goals)", int(df["is_high_scoring_fixture"].sum()))
    
    st.markdown("---")
    
    # Sidebar Filter Controls
    st.sidebar.header("Scouting Filters")
    selected_team = st.sidebar.selectbox("Isolate Specific Football Club", ["All Clubs"] + list(df["home_team"].unique()))
    
    display_df = df
    if selected_team != "All Clubs":
        display_df = df[(df["home_team"] == selected_team) | (df["away_team"] == selected_team)]
        
    st.subheader("📊 Goal Scoring Distribution Profiles")
    scoring_data = df.groupby("home_team")["home_score"].sum().sort_values(ascending=False)
    st.bar_chart(scoring_data)
    
    st.subheader("📋 Clean Processed Data Warehouse Table View")
    st.dataframe(display_df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Read Layer Linkage Exception: {e}")
