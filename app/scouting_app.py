import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Kirkland Data Systems Engine", layout="wide")

st.title("⚽ Premier League Analytics Framework")
st.markdown("### Production-Grade Cloud Analytics & Data Engineering Mart Interface")

db_path = "data/scouting_vault.duckdb"

try:
    conn = duckdb.connect(db_path, read_only=True)
    df = conn.execute("SELECT * FROM mart_scouting_fixtures").df()
    conn.close()
    
    # Display high-level metric cards
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Match Profiles Logged", len(df))
    m2.metric("Total Attacking Goal Actions", int(df["total_goals"].sum()))
    m3.metric("High Action Games (4+ Goals)", int(df["is_high_scoring_fixture"].sum()))
    
    st.markdown("---")
    
    # Interactive Sidebar Layout Controls
    st.sidebar.header("Scouting Parameter Filters")
    selected_club = st.sidebar.selectbox("Filter by Specific Football Club", ["All Clubs"] + list(df["home_team"].unique()))
    
    display_df = df
    if selected_club != "All Clubs":
        display_df = df[(df["home_team"] == selected_club) | (df["away_team"] == selected_club)]
        
    # Visual Charting Engine
    st.subheader("📊 Goal Aggregation Frequency Profiles")
    scoring_distribution = df.groupby("home_team")["home_score"].sum().sort_values(ascending=False)
    st.bar_chart(scoring_distribution)
    
    # Flat Data Table Matrix View
    st.subheader("📋 Production Datamart Ingestion Preview")
    st.dataframe(display_df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Data connection exception occurred: {e}. Please ensure python run_models.py has been executed to construct database files.")
