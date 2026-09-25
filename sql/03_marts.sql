SELECT 
    match_date,
    home_team,
    away_team,
    home_score,
    away_score,
    (home_score + away_score) as total_goals,
    CASE WHEN (home_score + away_score) >= 4 THEN 1 ELSE 0 END as is_high_scoring_fixture
FROM staging_matches;
