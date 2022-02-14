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
* 200 salary cap draft
* 100 free agent budget

## tooling

The tooling created to download and parse data is not the specific goal of this repo but the tools are interesting nonetheless and are worth a mention.

### setup with virtualenv

1. Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Check python version with `$ python -V`
    * make sure this matches what you installed. It might be installed as `python3` or `python3.9` etc.
3. `$ python3.9 -m pip install virtualenv`
4. `$ cd fantasy-football`
5. `$ python3.9 -m virtualenv venv39` (or whatever you want to name it)
6. `$ source venv39/bin/activate`
7. `$ python -m pip install -r requirements.txt`
    * this is using your python virtualenv so you can just use `python`

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

----------

## 2021-2022 season final results

**3rd place**

I didn't hit my goal but I'm pretty happy with this, especially with how much I learned this year.

I ended the regular season tied with the best record which gave me a first round bye and in that bye week I put up a lot more points than most other teams. Unfortunately I lost my next match up by around 9 points because DeVante Parker put up a donut and Tyreek Hill had a terrible showing (3ish points), most likely from continued fatigue because he had COVID the previous week.

If I had pulled out a win in the second round of the playoffs I still would have lost in the final round, but it would have been a good match. I would have scored 150 points which is a phenomenal showing in half PPR but the ultimate winner of our league had 180 points the last game. It was a historic end to the season and well deserved with players like Burrow and J.Taylor on his roster.

### positives

* Prepping for draft day is a good idea (duh) and resulted in a much better outcome
* Week-to-week roster management was better, though I did continually have the Rodgers/Mahomes conundrum
* Picking up Justin Jackson in week 16 got me the win, hands down
* Juggling defenses week-to-week felt weird but was the way to go
* Good resources:
    * FantasyPros - I used their expert consensus rankings a lot and also listened to their main podcast every week
    * Fantasy Football Today in 5 (CBS Sports) - This podcast is great because it is quick. It helped me keep a few names in my head of players to watch out for and with upcoming defense match ups
    * Fantasy Football Advice - I started listening to this podcast part way through the season. I thought it provided good advice and if I had the time to listen to both this and FantasyPros, it was helpful to have overlapping and conflicting opinions on players

### negatives

* I could have looked ahead a week or two and stashed defenses better, especially this year where some of the mismatches resulted in huge defensive points
* learn how to trade - I think I only took one trade opportunity and potentially had one near the trade deadline that would have set me up for success in the post-season. I also didn't initiate any trades myself. I need to get over the feeling of getting the wrong end of a deal and make trade assessments on the best information I can find.
    * For example I should have traded Kareem Hunt when we was overperforming but instead I held onto him until he got hurt
    * Same goes for Tyreek, though I think he would've have finished the season much better had he not gotten COVID

----------

## draft day resources

* `data/cheatsheet_2021.csv` - ESPN draft data merged with FantasyPros recommendations
* `data/sg_all_projections_2021.csv` - SG projections and notes for half PPR, 12 team
* `data.db` - maybe helpful for randomly looking up a player, though pro-football-reference might be faster
