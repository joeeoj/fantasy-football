#!/usr/bin/env python3
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


def parse_player_data(p: BoxPlayer) -> dict:
    return {
        'player_id': p.playerId,
        'player_name': p.name,
        'pos': p.position,
        'team': p.proTeam,
        'projected_points': p.projected_points,
        'current_position': p.slot_position,
        'eligible_slots': set(p.eligibleSlots),
    }


if __name__ == '__main__':
    league = League(league_id=LEAGUE_ID, year=YEAR)
    week = league.current_week
    print(f'Current week: {week}')

    box_scores = league.box_scores()
    lineup = get_lineup(box_scores, 19)
    players = [parse_player_data(p) for p in lineup]
