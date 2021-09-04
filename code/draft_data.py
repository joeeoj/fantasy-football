#!/usr/bin/env python3
import csv
from datetime import date
from pathlib import Path

from espn_api.football import League


LEAGUE_ID = 17588244
DATA_DIR = Path.cwd().parent / 'data'
DRAFT_HEADER = ['round_num', 'round_pick', 'overall_pick', 'team_id', 'team_abbr', 'team_name', 'nominating_team_name',
                'nominating_team_id', 'player_id', 'player_name', 'bid_amount']
YEAR = date.today().year if date.today().month in [9, 10, 11, 12] else (date.today().year - 1)


league = League(league_id=LEAGUE_ID, year=YEAR)
drafts = league.draft

results = []
for i, draft in enumerate(drafts, start=1):
    results.append([draft.round_num, draft.round_pick, i, draft.team.team_id, draft.team.team_abbrev,
                    draft.team.team_name, draft.nominatingTeam.team_name, draft.nominatingTeam.team_id, draft.playerId,
                    draft.playerName, draft.bid_amount])

with open(DATA_DIR / 'draft_data_2021.csv', 'wt') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(DRAFT_HEADER)
    csvwriter.writerows(results)
