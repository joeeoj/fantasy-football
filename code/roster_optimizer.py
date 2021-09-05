#!/usr/bin/env python3
import csv
from datetime import date
import os
from pathlib import Path

from espn_api.football import League
import keyring


LEAGUE_ID = 17588244
ESPN_USER_NAME = os.getenv('ESPN_USER_NAME')
ESPN_S2 = os.getenv('ESPN_S2')
SWID = os.getenv('SWID')

DATA_DIR = Path.cwd().parent / 'data'
YEAR = date.today().year if date.today().month in [9, 10, 11, 12] else (date.today().year - 1)


league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)
print(f'Current week: {league.current_week}')

power_rankings = league.power_rankings()
box_scores = league.box_scores()
