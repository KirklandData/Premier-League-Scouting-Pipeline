import streamlit as st
import duckdb
import pandas as pd
import os

st.set_page_config(page_title="Kirkland Data Engine", layout="wide")

st.title("⚽ Premier League Scouting Intelligence Matrix")
st.markdown("### Production-Ready Data Engineering Analytics Dashboard")

# Define our database and raw folder locations
db_path = "data/scouting_vault.duckdb"
raw_data_path = "data/raw/fixtures_snapshot.json"

# AUTOMATED CLOUD FIX: If the database does not exist on the server, build it inline
if not os.path.exists(db_path):
    st.info("📦 First-time deployment detected. Running internal SQL models...")
    
    # 1. Force download raw data if missing
    if not os.path.exists(raw_data_path):
        from extract.fetch_fixtures import fetch_live_data
        fetch_live_data()
        
    # 2. Trigger the orchestrator to build our 3 SQL layers
    from run_models import build_data_infrastructure
    build_data_infrastructure()
    st.success("✅ Database compiled successfully!")

# Now proceed with reading the clean data mart table safely
try:
    conn = duckdb.connect(db_path, read_only=True)
    df = conn.execute("SELECT * FROM mart_scouting_fixtures").df()
    conn.close()
    
    # Render High-Level Metric Cards
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Match Profiles Loaded", len(df))
    c2.metric("Total Goals Scored", int(df["total_goals"].sum()))
    c3.metric("High Action Outlier Games (4+ Goals)", int(df["is_high_scoring_fixture"].sum()))
    
    st.markdown("---")
    
    # Interactive Sidebar UI Filters
    st.sidebar.header("Scouting Filters")
    selected_team = st.sidebar.selectbox("Filter by Specific Football Club", ["All Clubs"] + list(df["home_team"].unique()))
    
    display_df = df
    if selected_team != "All Clubs":
        display_df = df[(df["home_team"] == selected_team) | (df["away_team"] == selected_team)]
        
    st.subheader("📊 Goal Scoring Volume Profiles")
    scoring_data = df.groupby("home_team")["home_score"].sum().sort_values(ascending=False)
    st.bar_chart(scoring_data)
    
    st.subheader("📋 Clean Processed Data Warehouse Table View")
    st.dataframe(display_df, use_container_width=True)

except Exception as e:
    st.error(f"❌ System Linkage Error: {e}")
