WITH deduplicated_scouting AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY match_id 
            ORDER BY match_date DESC
        ) as row_seq
    FROM staging_matches
)
SELECT 
    match_id,
    match_date,
    home_team,
    away_team,
    home_score,
    away_score,
    clean_attendance,
    (home_score + away_score) as total_goals,
    CASE WHEN (home_score + away_score) >= 4 THEN 1 ELSE 0 END as is_high_scoring_fixture
FROM deduplicated_scouting
WHERE row_seq = 1;

