SELECT 
    -- Double-check for both 2-digit and 4-digit year strings to ensure complete resilience
    COALESCE(
        TRY_STRPTIME(Date, '%d/%m/%y')::DATE,
        TRY_STRPTIME(Date, '%d/%m/%Y')::DATE
    ) as match_date,
    HomeTeam::VARCHAR as home_team,
    AwayTeam::VARCHAR as away_team,
    FTHG::INT as home_score,
    FTAG::INT as away_score
FROM read_csv('data/raw/*.csv', header=True, columns={'Date': 'VARCHAR', 'HomeTeam': 'VARCHAR', 'AwayTeam': 'VARCHAR', 'FTHG': 'VARCHAR', 'FTAG': 'VARCHAR'})
WHERE Date IS NOT NULL AND HomeTeam IS NOT NULL;
