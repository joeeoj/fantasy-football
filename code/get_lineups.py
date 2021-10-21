#!/usr/bin/env python3
import argparse
from collections import defaultdict
import csv
from datetime import date
from itertools import chain
import os
from pathlib import Path

from espn_api.football import League
from espn_api.football.box_player import BoxPlayer
from espn_api.football.box_score import BoxScore


LEAGUE_ID = 17588244
DATA_DIR = Path(__file__).parent.parent / 'data'
YEAR = date.today().year if date.today().month in [9, 10, 11, 12] else (date.today().year - 1)
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
    'D/ST': 1,
    'BE': 5,
    'IR': 1,
}


def parse_player_data(p: BoxPlayer) -> dict:
    slots = set([e for e in p.eligibleSlots if (e in LEAGUE_SLOTS.keys() and e not in NOT_PLAYING)])

    return {
        'player_id': p.playerId,
        'player_name': p.name,
        'pos': p.position,
        'team': p.proTeam,
        'projected_points': p.projected_points,
        'points': p.points,
        'current_position': p.slot_position if p.slot_position != 'RB/WR/TE' else 'FLEX',
        'QB': 'QB' in slots, 
        'RB': 'RB' in slots, 
        'WR': 'WR' in slots, 
        'TE': 'TE' in slots, 
        'FLEX': 'RB/WR/TE' in slots, 
        'K': 'K' in slots, 
        'DST': 'D/ST' in slots,
    }


def parse_lineups(box_score: BoxScore, week: int) -> list[BoxPlayer]:
    home_team = box_score.home_team
    home_lineup = box_score.home_lineup

    away_team = box_score.away_team
    away_lineup = box_score.away_lineup

    players = []
    for player in home_lineup:
        p = parse_player_data(player)
        p['week'] = week
        p['fantasy_team_id'] = home_team.team_id
        p['fantasy_team_name'] = home_team.team_name
        p['opponent_team_id'] = away_team.team_id
        p['opponent_team_name'] = away_team.team_name
        p['home_away'] = 'home'
        players.append(p)

    for player in away_lineup:
        p = parse_player_data(player)
        p['week'] = week
        p['fantasy_team_id'] = away_team.team_id
        p['fantasy_team_name'] = away_team.team_name
        p['opponent_team_id'] = home_team.team_id
        p['opponent_team_name'] = home_team.team_name
        p['home_away'] = 'away'
        players.append(p)

    return players


def download_and_save(current_week: int, week: int) -> None:
    print(f' Current week: {current_week}')
    print(f'Week to parse: {week}')

    box_scores = league.box_scores(week=week)
    lineups = list(chain.from_iterable([parse_lineups(bs, week) for bs in box_scores]))
    print(f'Players parsed: {len(lineups):,}')

    fout = DATA_DIR / f'lineups_week_{week:02}.csv'
    print(f'Saving to {fout.name}')
    with open(fout, 'wt') as f:
        csvwriter = csv.DictWriter(f, fieldnames=lineups[0].keys())
        csvwriter.writeheader()
        csvwriter.writerows(lineups)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('lineup', description='Get weekly lineups')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all', help='Download all weeks', action='store_true')
    group.add_argument('--week', help='Week to download (default is the current week)', type=int)
    args = parser.parse_args()

    league = League(league_id=LEAGUE_ID, year=YEAR)
    current_week = league.current_week
    week = current_week if args.week is None or args.week == current_week else args.week

    if args.all:
        for week in range(1, current_week+1):
            download_and_save(current_week, week)
    else:
        download_and_save(current_week, week)
