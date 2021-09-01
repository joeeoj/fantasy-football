# fantasy football

Most of this is 2021 focused. We'll see how much of it "works" and is transferable to next year.

[Project documentation](https://joeeoj.github.io/fantasy-football/)

## what is this

The whole point of this repo is to win at (NFL) fantasy football this year. I'm coming in with a weak understanding of salary cap auctions and no idea how to do matchups or find good fliers mid-season so there is a lot to learn. As a result the documentation contains misc notes on strategy I've been able to find online.

The current goal (besides learning) is to generate projections that include player values, ranks, and tiers (by position). Hopefully I'll have a bit of time left to also try some mock drafts and come up with a few probable team configurations.

### 2021 league settings

* 12 teams
* 6pt rush/rec TD and 4pt pass TD
* half PPR
* 1 QB / 2 RB / 3 WR / 1 TE / 1 FLEX / 1 K / 1 DST
* 5 bench / 1 IR
* $200 salary cap draft
* $100 free agent budget

## tooling

The tooling created to download and parse data is not the specific goal of this repo but the tools are interesting nonetheless and are worth a mention.

### `code/league_data.py`

This parses historical league data from my actual league or projections for the current year. I didn't participate last year and we didn't have the league in 2019 so the historical data is of limited use. The 2021 projections are helpful, though, because they are based on our current league settings.

It can be repurposed for different ESPN leagues by changing the `LEAGUE_ID` variable

### `code/get_pro_football_ref_players.py`

Command line script that parses historical pro-football-reference data for the top 600-ish players for a given year. It also calculates the half PPR points for our league (coincidentally the same as the FanDuel points). This is the source of historical player performance.

### `code/make_db_and_load_data.sh`

This runs the `create_tables.sql` script to create a sqlite database called `data.db` that contains most of the stuff in `data/`. It currently has the following tables:

* players - using the pro-football-reference historical player data
* teams
* byes
* injuries
* strength_of_schedule

It provides a convenient way to query the data and also enforces foreign key relations between some of the tables.

### `code/espn_draft_trends.py`

Parses the [ESPN Live Draft Trends](https://fantasy.espn.com/football/livedraftresults) with a focus on PPR and Salary Cap data.
