#!/usr/bin/env python3
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

from espn_api.football import League, Player


DATA_DIR = Path.cwd().parent / 'data'
LEAGUE_ID = 17588244
PLAYER_HEADER = ['id', 'name', 'position', 'total_points']


@dataclass
class Player:
    player_id: int
    name: str
    pos: str
    total_points: float

    def __iter__(self):
        """https://stackoverflow.com/a/37382942"""
        return iter([self.player_id, self.name, self.pos, self.total_points])


def players_to_csv(players: List[Player], fout: str = 'players.csv') -> None:
    with open(DATA_DIR / fout, 'wt') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(PLAYER_HEADER)
        for p in players:
            csvwriter.writerow(list(p))


def download_all_players() -> List[Player]:
    """Get both rostered players and free agents and put them in one list"""
    everyone, parsed = [], []

    # get all rostered and unrostered even if there are dupes
    for team in league.teams:
        for player in team.roster:
            everyone.append(player)

    for player in league.free_agents(size=1_000):
        everyone.append(player)

    # parse into smaller dataclass
    for p in everyone:
        player = Player(p.playerId, p.name, p.position, p.total_points)
        parsed.append(player)

    return parsed


if __name__ == '__main__':
    league = League(league_id=LEAGUE_ID, year=2020)
    players = download_all_players()

    print(f'Total players: {len(players):,}')
    players_to_csv(players, 'player_points_2020.csv')
