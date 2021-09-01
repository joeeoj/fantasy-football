CREATE TABLE players (
    player_id TEXT,
    name TEXT,
    team TEXT,
    fantasy_pos TEXT,
    age INTEGER,
    g INTEGER,
    gs INTEGER,
    pass_cmp INTEGER,
    pass_att INTEGER,
    pass_yds INTEGER,
    pass_td INTEGER,
    pass_int INTEGER,
    rush_att INTEGER,
    rush_yds INTEGER,
    rush_yds_per_att REAL,
    rush_td INTEGER,
    targets INTEGER,
    rec INTEGER,
    rec_yds INTEGER,
    rec_yds_per_rec REAL,
    rec_td INTEGER,
    fumbles INTEGER,
    fumbles_lost INTEGER,
    all_td INTEGER,
    two_pt_md INTEGER,
    two_pt_pass INTEGER,
    fantasy_points REAL,
    fantasy_points_ppr REAL,
    draftkings_points REAL,
    fanduel_points REAL,
    vbd INTEGER,
    fantasy_rank_pos INTEGER,
    fantasy_rank_overall INTEGER,
    year INTEGER,
    half_ppr REAL,
    pos_rank INTEGER,

    PRIMARY KEY (player_id, year, fantasy_pos)
);

CREATE TABLE teams (
    official_team_abbr TEXT PRIMARY KEY,
    other_team_abbr TEXT,
    pro_football_ref_abbr TEXT,
    fullname TEXT,
    active INTEGER,
    FOREIGN KEY (pro_football_ref_abbr) REFERENCES players (team)
);

CREATE TABLE byes (
    team_abbr TEXT PRIMARY KEY,
    bye INTEGER,
    FOREIGN KEY (team_abbr) REFERENCES teams (official_team_abbr)
);

CREATE TABLE strength_of_schedule (
    rank INTEGER,
    team TEXT PRIMARY KEY,
    team_abbr TEXT,
    opponents_combined_2020_record TEXT,
    opponents_combined_2020_win_pct REAL,
    FOREIGN KEY (team_abbr) REFERENCES teams (official_team_abbr)
);

CREATE TABLE injuries (
    year INTEGER,
    player_id TEXT,
    name TEXT,
    position TEXT,
    team TEXT,
    est_missed_games INTEGER,
    notes TEXT,

    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (team) REFERENCES teams (official_team_abbr)
);

.separator ","

.import --csv --skip 1 ../data/teams.csv teams

.import --csv --skip 1 ../data/players_2016.csv players
.import --csv --skip 1 ../data/players_2017.csv players
.import --csv --skip 1 ../data/players_2018.csv players
.import --csv --skip 1 ../data/players_2019.csv players
.import --csv --skip 1 ../data/players_2020.csv players

.import --csv --skip 1 ../data/byes.csv byes

.import --csv --skip 1 ../data/strength_of_schedule.csv strength_of_schedule

.import --csv --skip 1 ../data/injuries.csv injuries

CREATE INDEX IX_players_year_team ON players (year, team);
CREATE INDEX IX_players_pos ON players (fantasy_pos);
CREATE INDEX IX_players_year_pos ON players (year, fantasy_pos);

PRAGMA foreign_keys=true;

VACUUM;
