SELECT 
    match_id,
    CAST(match_date AS DATE) as match_date,
    TRIM(home_team) as home_team,
    TRIM(away_team) as away_team,
    home_score,
    away_score,
    COALESCE(attendance, 0) as clean_attendance
FROM raw_matches
WHERE 
    home_score IS NOT NULL 
    AND away_score IS NOT NULL;

