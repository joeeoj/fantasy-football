# data

`make_db_and_load_data.sh` - This bash script creates a SQLite database called `data.db` in the `data/` folder using `create_tables.sql`

## tables

### projections (TBD)

Might parse one or all of these sources to use for projections or put them all together to compare side-by-side.

* [espn draft trends](https://fantasy.espn.com/football/livedraftresults)
* [thefootballgirl](https://thefootballgirl.com/fitz-on-fantasy-2021-fantasy-draft-rankings/)
* [fantasypros](https://www.fantasypros.com/nfl/rankings/half-point-ppr-rb-cheatsheets.php?loggedin)

### players

This contains historical player data pulled from pro-football-reference using `get_pro_football_ref_players.py`

These are saved as separate csv files in `data/` each named `players_<year>.csv`.

### teams

Contains a list of official and unofficial team abbreviations and names from wikipedia[^1]

### byes

manually pulled from nfl.com[^2]

### strength_of_schedule

downloaded from 4for4.com[^3]

### injuries

Manually pulled from FantasyPros[^4] and the Philly Voice[^5]...(because it showed up on Google)

[^1]: [WikiProject National Football League/National Football League team abbreviations](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Football_League/National_Football_League_team_abbreviations)
[^2]: [NFL 2021 bye weeks](https://www.nfl.com/news/how-bye-weeks-break-down-in-nfl-s-17-game-2021-season)
[^3]: [2021 NFL strength of schedule](https://www.4for4.com/teams/schedule/2021/grid)
[^4]: [FantasyPros injury news](https://www.fantasypros.com/nfl/injury-news.php)
[^5]: [PhillyVoice injury updates](https://www.phillyvoice.com/fantasy-football-injuries-updates-draft-advuce-jk-dobbins-darrell-henderson-ceedee-lamb-dandre-swift-raheem-mostert/)
