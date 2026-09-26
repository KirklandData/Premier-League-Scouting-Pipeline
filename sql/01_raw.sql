SELECT
    ROW_NUMBER() OVER (ORDER BY match_date) AS match_id,
    match_date,
    HomeTeam AS home_team,
    AwayTeam AS away_team,
    TRY_CAST(FTHG AS INTEGER) AS home_score,
    TRY_CAST(FTAG AS INTEGER) AS away_score,
    NULL AS attendance  -- this free public results feed does not publish official attendance figures
FROM (
    SELECT
        *,
        COALESCE(
            TRY_STRPTIME(Date, '%d/%m/%Y'),
            TRY_STRPTIME(Date, '%d/%m/%y')
        )::DATE AS match_date
    FROM read_csv('data/raw/fixtures_snapshot.csv', header=True, types={'Date': 'VARCHAR'})
)
WHERE HomeTeam IS NOT NULL AND AwayTeam IS NOT NULL;
