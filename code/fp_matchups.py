#!/usr/bin/env python3
"""Parse FantasyPros matchups by position and player into a flat format

https://www.fantasypros.com/nfl-matchup-ratings/
"""
import csv
from pathlib import Path

import bs4
import requests


POSITIONS = ['qb', 'rb', 'wr', 'te', 'k', 'dst']
URL = 'https://www.fantasypros.com/nfl/matchups/{pos}.php'

# ECR = expert consensus ranking
HEADER = ['ecr', 'pos', 'player_name', 'team', 'week', 'matchup_rating', 'opponent', 'opponent_rank', 'home_away']
DATA_DIR = Path.cwd().parent / 'data'


def count_stars(cell: bs4.element.Tag) -> int:
    """1 to 5 scale of easy of matchup where 1 is hard and 5 is easy"""
    if cell.text == 'BYE':
        return None

    items = [s.attrs.get('class') for s in cell.find_all('i')]
    count = sum([0 if 'bad-star' in item else 1 for item in items])
    return count


def get_rows_by_pos(pos: str) -> bs4.element.ResultSet:
    """Download table for given position, parse table, then return rows"""
    soup = bs4.BeautifulSoup(requests.get(URL.format(pos=pos)).content, 'lxml')
    table = soup.find('table', id='data')
    rows = table.find_all('tr')
    return rows


if __name__ == '__main__':
    results = []
    for pos in POSITIONS:
        print(pos)
        rows = get_rows_by_pos(pos)
        for row in rows[1:]:
            cells = row.find_all('td')

            ecr = int(cells[0].text)
            team = cells[1].small.text
            player_name = cells[1].find('a', class_='fp-player-link').attrs.get('fp-player-name')

            for i in range(1, 19):
                week = i
                matchup_rating = count_stars(cells[i+1])

                opponent, home_away, opponent_rank = None, None, None
                if cells[i+1].span:
                    opponent = cells[i+1].find('div', class_='wk').text
                    
                    if 'vs' in opponent:
                        home_away = 'home'
                    elif 'at' in opponent:
                        home_away = 'away'

                    opponent = opponent.replace('vs.', '').replace('at', '').strip()
                    opponent_rank = int(cells[i+1].span.attrs.get('data-rank'))

                results.append([ecr, pos.upper(), team, player_name, week, matchup_rating, opponent, opponent_rank,
                                home_away])


    with open(DATA_DIR / 'fp_matchups_2021.csv', 'wt') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(HEADER)
        csvwriter.writerows(results)
