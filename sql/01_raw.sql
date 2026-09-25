SELECT 
    -- Explicitly cast the Date column to text (VARCHAR) before stripping the date format
    TRY_STRPTIME(Date::VARCHAR, '%d/%m/%Y')::DATE as match_date,
    HomeTeam::VARCHAR as home_team,
    AwayTeam::VARCHAR as away_team,
    FTHG::INT as home_score,
    FTAG::INT as away_score
FROM read_csv_auto('data/raw/*.csv');
