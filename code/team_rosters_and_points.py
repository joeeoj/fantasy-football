#!/usr/bin/env python3
import argparse
from collections import defaultdict
import csv
from datetime import date
import json
from typing import List

from espn_api.football import League
from espn_api.football.box_player import BoxPlayer
from espn_api.football.box_score import BoxScore


LEAGUE_ID = 17588244
YEAR = date.today().year if date.today().month in [9, 10, 11, 12] else (date.today().year - 1)


def print_scores(box_scores: List[BoxScore]) -> None:
    for scores in box_scores:
        home_score, away_score = scores.home_score, scores.away_score
        home, away = scores.home_team, scores.away_team
        print(f'{home.team_name:>30}: {home_score:>6}')
        print(f'{away.team_name:>30}: {away_score:>6}')
        print('-' * 50)


def parse_player(player: BoxPlayer) -> dict:
    return {
        'id': player.playerId,
        'name': player.name,
        'team': player.proTeam,
        'position': player.position,
        'slot_position': player.slot_position,
        'injury_status': player.injuryStatus,
        'actual_points': player.points,
        'projected_points': player.projected_points,
        'points_breakdown': player.points_breakdown,
    }


def parse_roster(scores: List[BoxPlayer]) -> dict:
    roster = defaultdict(list)
    for player in scores:
        d = parse_player(player)
        roster[d.get('slot_position')].append(d)
    return roster


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='points', description='Get rosters and points as json')
    parser.add_argument('--verbose', '-v', help='Print point summaries by team', action='store_true')
    parser.add_argument('--fout', help='Write json to file (format: week_<num>_points.json)', action='store_true')
    args = parser.parse_args()

    league = League(league_id=LEAGUE_ID, year=YEAR)
    box_scores = league.box_scores()
    week = league.current_week

    if args.verbose:
        print(f'Current week: {week}')
        print_scores(box_scores)

    if args.fout:
        teams = {}
        for scores in box_scores:
            teams[scores.home_team.team_id] = parse_roster(scores.home_lineup)
            teams[scores.away_team.team_id] = parse_roster(scores.away_lineup)

        fout = f'week_{week:>02}_points.json'
        with open(fout, 'wt') as f:
            json.dump(teams, f, indent=2)
