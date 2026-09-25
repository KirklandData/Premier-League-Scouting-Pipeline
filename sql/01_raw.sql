SELECT 
    -- Read columns by their position index to completely bypass header spelling issues
    COALESCE(
        TRY_STRPTIME(column0::VARCHAR, '%d/%m/%y')::DATE,
        TRY_STRPTIME(column0::VARCHAR, '%d/%m/%Y')::DATE
    ) as match_date,
    column1::VARCHAR as home_team,
    column2::VARCHAR as away_team,
    column3::INT as home_score,
    column4::INT as away_score
FROM read_csv('data/raw/fixtures_snapshot.csv', 
              header=False, 
              skip=1,
              delim=',', 
              auto_detect=True);
