SELECT 
    element.match_id::INT as match_id,
    element.match_date::VARCHAR as match_date,
    element.home_team.home_team_name::VARCHAR as home_team,
    element.away_team.away_team_name::VARCHAR as away_team,
    element.home_score::INT as home_score,
    element.away_score::INT as away_score,
    element.attendance::INT as attendance
FROM read_json_auto('data/raw/*.json') as element;
