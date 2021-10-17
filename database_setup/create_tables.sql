CREATE TABLE lineups (
    player_id INTEGER,
    player_name TEXT,
    pos TEXT,
    team TEXT,
    projected_points NUMERIC(4, 2),
    points NUMERIC(4, 2),
    current_position TEXT,
    QB BOOLEAN,
    RB BOOLEAN,
    WR BOOLEAN,
    TE BOOLEAN,
    FLEX BOOLEAN,
    K BOOLEAN,
    DST BOOLEAN,
    week SMALLINT,
    fantasy_team_id SMALLINT,
    fantasy_team_name TEXT,
    opponent_team_id SMALLINT,
    opponent_team_name TEXT,
    home_away TEXT,

    PRIMARY KEY(player_id, fantasy_team_id, week)
);

CREATE INDEX lineups_pos_index ON lineups (pos);
CREATE INDEX lineups_team_index ON lineups (team);

CREATE VIEW projected_vs_actual AS
SELECT
    player_id
    ,player_name
    ,pos
    ,current_position
    ,team
    ,week
    ,fantasy_team_id
    ,fantasy_team_name
    ,projected_points
    ,points
    ,points - projected_points as diff
FROM lineups
;