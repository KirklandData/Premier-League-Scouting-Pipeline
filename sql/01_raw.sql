SELECT 
    -- Double-check for both 2-digit and 4-digit variations to ensure complete resilience
    COALESCE(
        TRY_STRPTIME(Date::VARCHAR, '%d/%m/%y')::DATE,
        TRY_STRPTIME(Date::VARCHAR, '%d/%m/%Y')::DATE
    ) as match_date,
    HomeTeam::VARCHAR as home_team,
    AwayTeam::VARCHAR as away_team,
    FTHG::INT as home_score,
    FTAG::INT as away_score
FROM read_csv('data/raw/fixtures_snapshot.csv', 
              header=True, 
              delim=',', 
              auto_detect=True, 
              ignore_errors=True);
