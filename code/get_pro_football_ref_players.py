#!/usr/bin/env python3
import argparse
import csv
from typing import List, Union

from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests


BASE_URL = 'https://www.pro-football-reference.com'


def calc_fantasy_points(p: dict, ppr: float = 0.0) -> float:
    """https://www.fantasypros.com/scoring-settings/
    assumes player dict from pro-football-reference"""
    passing = p.get('pass_yds') / 25
    rushing = p.get('rush_yds') / 10
    receiving = p.get('rec_yds') / 10

    tds = (p.get('rush_td') + p.get('rec_td')) * 6
    tds += p.get('pass_td') * 4
    tds += (p.get('two_pt_md') + p.get('two_pt_pass')) * 2

    # extra tds like punt returns
    extra = p.get('all_td') - p.get('rush_td') - p.get('rec_td')
    tds += (extra * 6)

    half_ppr = p.get('rec') * ppr

    lost = p.get('pass_int') +  (p.get('fumbles_lost') * 2)

    return round(passing + rushing + receiving + tds + half_ppr - lost, 1)


def try_parse_num(s: str) -> Union[float, int, str]:
    """Attempt to parse string into float or int, otherwise return the input str"""
    if s.strip() == '':
        return 0

    if '.' in s:
        try:
            return float(s)
        except ValueError:
            pass
    else:
        try:
            return int(s)
        except ValueError:
            pass
    return s


def parse_player_row(cells: ResultSet) -> dict:
    d = {}

    p = cells[0]
    d['player_id'] = p.a.get('href').replace('.htm', '').split('/')[-1]
    d['name'] = p.a.text.strip()

    for cell in cells[1:]:  # skip first cell
        data_stat = cell.attrs.get('data-stat')
        d[data_stat] = try_parse_num(cell.text)

    return d


def download_players(year: int) -> List[dict]:
    url = f'{BASE_URL}/years/{year}/fantasy.htm'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')[2:]  # skip headers

    players = []
    for row in rows:
        cells = row.find_all('td')
        if cells:
            player = parse_player_row(cells)
            player['year'] = year

            # filter out players without a position
            if not player.get('fantasy_pos'):
                continue

            # add points with half PPR for my leauge
            player['half_ppr'] = calc_fantasy_points(player, ppr=0.5)
            players.append(player)

    # add pos rank based on half_ppr
    with_ranks = []
    for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'P', 'D/ST', 'DT']:
        by_pos = sorted([p for p in players if p.get('fantasy_pos') == pos], key=lambda p: p.get('half_ppr'), reverse=True)
        for p, i in zip(by_pos, range(1, len(by_pos)+1)):
            p['pos_rank'] = i
        with_ranks.extend(by_pos)

    return with_ranks


def save_to_csv(players: List[dict], fout: str) -> None:
    with open(fout, 'wt') as f:
        csvwriter = csv.DictWriter(f, fieldnames=players[0].keys())
        csvwriter.writeheader()
        csvwriter.writerows(players)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='fbdata',
                                     description='Download yearly player data from pro-football-reference',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('year', type=int, help='Year to download')
    parser.add_argument('--fout', help='Change default csv name', default=f'players_<year>.csv')
    args = parser.parse_args()

    players = download_players(args.year)
    print(f'Total players: {len(players):,}')

    fout = f'players_{args.year}.csv' if args.fout == 'players_<year>.csv' else args.fout
    save_to_csv(players, fout)
