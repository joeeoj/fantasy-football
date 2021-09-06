#!/usr/bin/env python3
from collections import defaultdict
import csv
from datetime import date
import os
from pathlib import Path

from espn_api.football import League
from espn_api.football.box_player import BoxPlayer
from espn_api.football.box_score import BoxScore


LEAGUE_ID = 17588244
DATA_DIR = Path.cwd().parent / 'data'
YEAR = date.today().year if date.today().month in [9, 10, 11, 12] else (date.today().year - 1)
TEAMS = {
    1: 'Fully  Maccinated',
    2: "Rippin' Swigs",
    3: 'Seattle Fantasy Team',
    10: 'Spenny Willy',
    11: 'Raiders Are Good',
    12: 'Herb Your Enthusiasm',
    13: 'Too Many Cooks',
    15: 'Elite starts  with Eli',
    16: 'Draftin Herbert First Pick',
    17: 'Scooty Lewis and the News',
    18: 'Team barrett',
    19: 'Federal Way Yu',
 }
NOT_PLAYING = set(['BE', 'IR'])  # non-playing slots

# RB/WR/TE = FLEX
# we do not have OP, RB/WR, WR/TE, or Rookie
LEAGUE_SLOTS = {
    'QB': 1,
    'RB': 2,
    'WR': 3,
    'TE': 1,
    'RB/WR/TE': 1,
    'K': 1,
    'DST': 1,
    'BE': 5,
    'IR': 1,
}


def get_lineup(box_scores: BoxScore, team_id: int) -> list[BoxPlayer]:
    """Parse lineup for a given team id"""
    for scores in box_scores:
        if scores.home_team.team_id == team_id:
            print('home')
            lineup = scores.home_lineup
            break
        elif scores.away_team.team_id == team_id:
            print('away')
            lineup = scores.away_lineup
            break

    return lineup


def parse_player_data(p: BoxPlayer, team_id: int) -> dict:
    return {
        'fantasy_team_id': team_id,
        'player_id': p.playerId,
        'player_name': p.name,
        'pos': p.position,
        'team': p.proTeam,
        'projected_points': p.projected_points,
        'current_position': p.slot_position,
        'eligible_slots': set(p.eligibleSlots),
    }


# if __name__ == '__main__':
league = League(league_id=LEAGUE_ID, year=YEAR)
week = league.current_week
print(f'Current week: {week}')

box_scores = league.box_scores()
longest_team_name = max([len(v) for v in TEAMS.values()])

for matchup in box_scores:
    home = matchup.home_team
    away = matchup.away_team
    print(f'{away.team_name:>{longest_team_name}} ({away.team_id:>2}) at {home.team_name} ({home.team_id})')

team_id = 19
lineup = get_lineup(box_scores, team_id)
players = [parse_player_data(p, team_id) for p in lineup]
projected = round(sum([p['projected_points'] for p in players if p['current_position'] not in NOT_PLAYING]), 2)


players_per_slots = defaultdict(list)
for player in players:
    eligible_slots = player.get('eligible_slots')
    for slot in eligible_slots:
        if slot in LEAGUE_SLOTS.keys() and slot not in NOT_PLAYING:
            players_per_slots[slot].append(player)

for pos, players in players_per_slots.items():
    print(f'{pos}: {len(players):,}')
