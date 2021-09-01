#!/usr/bin/env python3
import argparse
import csv
import json
from math import floor
from typing import List

import requests


URL = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leaguedefaults/3?view=kona_player_info'
# ty -- https://reddit.com/im6mui
FILTERS = {
    "players": {
        "limit": 1_500,
        "sortDraftRanks": {
            "sortPriority": 100,
            "sortAsc": True,
            "value": "PPR"
        }
    }
}
HEADERS = {'x-fantasy-filter': json.dumps(FILTERS)}
POSITIONS = {
    1: 'QB',
    2: 'RB',
    3: 'WR',
    4: 'TE',
    5: 'K',
    16: 'DST',
}


def download_data(year: int) -> List[dict]:
    url = URL.format(year=year)
    r = requests.get(url, headers=HEADERS)
    return r.json().get('players')


def parse_player(p: dict) -> dict:
    player = p.get('player')
    ownership = player.get('ownership')

    if player is None or ownership is None:
        return None

    ppr_auc_value = floor(player.get('draftRanksByRankType').get('PPR').get('auctionValue', 0))
    avg_auc_value = floor(ownership.get('auctionValueAverage', 0))

    ppr_rank = player.get('draftRanksByRankType').get('PPR').get('rank')
    avg_draft_post = floor(ownership.get('averageDraftPosition'))

    return {
        'player_id': player.get('id'),
        'name': player.get('fullName'),
        'pos': POSITIONS.get(player.get('defaultPositionId')),
        'ppr_rank': ppr_rank,
        'avg_draft_pos': avg_draft_post,
        'pos_diff': avg_draft_post - ppr_rank,
        'ppr_auc_value': ppr_auc_value,
        'avg_auc_value': avg_auc_value,
        'auc_diff': avg_auc_value - ppr_auc_value,
    }


def write_to_csv(players: List[dict], fout: str) -> None:
    with open(fout, 'wt') as f:
        csvwriter = csv.DictWriter(f, fieldnames=players[0].keys())
        csvwriter.writeheader()
        csvwriter.writerows(players)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='espn-trends', description='Download ESPN FF draft trends to csv',
                                     formatter_class= argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('year', help='Year to download', type=int)
    parser.add_argument('--fout', help='Output file name', default='espn_draft_trends_{year}.csv')
    args = parser.parse_args()
    
    players = download_data(args.year)
    print(f'Total players: {len(players):,}')

    parsed = [parse_player(p) for p in players if parse_player(p) is not None]
    print(f'Total parsed players: {len(parsed):,}')

    fout = args.fout.format(year=args.year) if '{year}' in args.fout else args.fout
    write_to_csv(parsed, fout)
