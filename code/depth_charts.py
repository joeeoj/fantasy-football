#!/usr/bin/env python3
"""Download and parse NFL depth charts from the Huddle into flattened format (one row per player)"""
import csv
from pathlib import Path

import bs4
import requests


DATA_DIR = Path.cwd().parent / 'data'
URL = 'https://tools.thehuddle.com/nfl-depth-charts'
LEGEND = {
    '(N)': 'New to Team',
    '(R)': 'Rookie',
    '(IR)': 'Injured Reserve',
    '(PUP)': 'Physically Unable to Perform',
    '(IR-R)': 'Injured Reserve w/ opportunity to return',
    '(SUS)': 'Suspended',
}
POS_ORDER = ['QB', 'RB', 'WR', 'TE', 'K']


def download_table(url: str) -> bs4.element.ResultSet:
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    table = soup.find_all(attrs={'data-reactid': 314})
    rows = soup.find_all('tr')
    # header = [item.text for item in rows[0].find_all('th')]  # don't need

    return rows


def parse_row(row: bs4.element.Tag) -> list[list[str]]:
    results = []
    for col in row.find_all('td'):
        col_results = []
        for item in col.find_all('a'):
            val = item.text.strip()
            col_results.append(item.text.strip())
        results.append(col_results)
    return results


def parse_qualifier(val: str) -> tuple[str, list[str]]:
    s, qualifiers = val, []
    for k,v in LEGEND.items():
        if k in val:
            s = s.replace(k, '').strip()
            qualifiers.append(v)
    return (s, qualifiers)


def write_to_csv(players: list[str, list[str]]) -> None:
    output_header = ['team', 'pos', 'depth', 'player', 'qualifiers']
    with open(DATA_DIR / 'depth_chart_2021.csv', 'wt') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(output_header)

        for row in players:
            qualifiers = ' | '.join(row[-1])
            csvwriter.writerow(row[:-1] + [qualifiers])


if __name__ == '__main__':
    rows = download_table(URL)

    parsed_rows = [parse_row(row) for row in rows if len(parse_row(row)) > 0]
    assert len(parsed_rows) == 32  # only 32 teams

    # team, pos, depth, player, qualifiers
    flattened_results = []
    for row in parsed_rows:
        team, player_cols = row[0], row[1:]
        for pos, players in zip(POS_ORDER, player_cols):
            for i, p in enumerate(players, start=1):
                player_fixed, qualifiers = parse_qualifier(p)
                flattened_results.append([team[0], pos, i, player_fixed, qualifiers])

    write_to_csv(flattened_results)
