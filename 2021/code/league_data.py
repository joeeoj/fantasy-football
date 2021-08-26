#!/usr/bin/env python3
"""CLI to get all player data for ESPN NFL fantasy football. League id is hardcoded, year is configurable."""
import argparse
import copy
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List

from espn_api.football import League


LEAGUE_ID = 17588244
PLAYER_HEADER = ['id', 'name', 'position', 'team', 'total_points', 'projected_total_points', 'rank']
YEAR = date.today().year


@dataclass
class Player:
    player_id: int
    name: str
    pos: str
    team: str
    total_points: float
    projected_total_points: float
    rank: int = None

    def __iter__(self):
        """https://stackoverflow.com/a/37382942"""
        return iter([self.player_id, self.name, self.pos, self.team, self.total_points, self.projected_total_points,
                     self.rank])


def save_players_to_csv(players: List[Player], fout: str) -> None:
    with open(fout, 'wt') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(PLAYER_HEADER)
        for p in players:
            csvwriter.writerow(list(p))


def download_all_players(league: League) -> List[Player]:
    """Get both rostered players and free agents and put them in one list"""
    everyone, parsed = [], []

    # get all rostered and unrostered
    for team in league.teams:
        for player in team.roster:
            everyone.append(player)

    for player in league.free_agents(size=2_000):
        everyone.append(player)

    # parse into smaller dataclass, rank added later
    for p in everyone:
        player = Player(p.playerId, p.name, p.position, p.proTeam, p.total_points, p.projected_total_points)
        parsed.append(player)

    return parsed


def rank_by_position(players: List[Player], rank_col: str) -> List[Player]:
    players_copy = [copy.deepcopy(p) for p in players]  # avoid mutating in place

    for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'P', 'D/ST', 'DT']:
        by_pos = sorted([p for p in players_copy if p.pos == pos], key=lambda p: getattr(p, rank_col), reverse=True)
        for p, i in zip(by_pos, range(1, len(by_pos)+1)):
            p.rank = i

    return players_copy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='ff-data', description='Download ESPN FF player data',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--year', help='FF year', default=YEAR)
    parser.add_argument('--fout', help='Save player data to csv', default='players.csv')
    parser.add_argument('--rank', help='Rank by total/actual or projected points',
                        choices=['total_points', 'projected_total_points'], default='projected_total_points')
    args = parser.parse_args()

    league = League(league_id=LEAGUE_ID, year=int(args.year))

    teams = league.teams
    print(f'Total FF teams: {len(teams):,}')

    players = download_all_players(league)
    print(f'Total parsed players: {len(players):,}')

    ranked_players = rank_by_position(players, args.rank)

    save_players_to_csv(ranked_players, args.fout)
