#!/usr/bin/env python3
import argparse
from collections import namedtuple
import csv
from datetime import date, datetime
import os
from pytz import timezone
from pathlib import Path

from espn_api.football import League


LEAGUE_ID = 17588244

# https://github.com/rbarton65/espnff/issues/28
# needed to read recent activity otherwise you'll get a 401
ESPN_S2 = os.getenv('ESPN_S2')
SWID = os.getenv('SWID')

DATA_DIR = Path.cwd().parent / 'data'
YEAR = date.today().year if date.today().month in [9, 10, 11, 12] else (date.today().year - 1)
TZ = timezone('America/Los_Angeles')
DT_FORMAT = '%A %b %d, %Y at %I:%M %p %Z'


ACTION_HEADER = ['datetime', 'team_id', 'team_name', 'player_name', 'player_id', 'cost', 'move']
Action = namedtuple('Action', ACTION_HEADER)


def localize_activity_ts(ts: int) -> str:
    dt = datetime.fromtimestamp(ts/1000)
    return TZ.localize(dt)


def write_to_csv(actions: list[Action], fout: str) -> None:
    with open(fout, 'wt') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(ACTION_HEADER)
        csvwriter.writerows(actions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='activity', description='print out recent league activity (Add, Drop, Trade)')
    parser.add_argument('--limit', type=int, default=25, help='activity limit (default %(default)s)')
    parser.add_argument('--fout', help='Export to csv')
    args = parser.parse_args()

    league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)

    recent_activity = league.recent_activity(size=args.limit)

    parsed_actions, output = [], ''
    for activity in recent_activity:
        dt = localize_activity_ts(activity.date)
        output += dt.strftime(DT_FORMAT) + '\n'

        for action in activity.actions:
            team, move, player, cost = action
            a = Action(dt, team.team_id, team.team_name, player.name, player.playerId, cost, move)
            parsed_actions.append(a)

            output += f'${a.cost:>2} - {a.team_name} {a.move} {a.player_name} ({a.player_id})\n'
        output += ('-' * 80) + '\n'

    if args.fout:
        write_to_csv(parsed_actions, args.fout)
    else:
        # print unless writing to csv
        print(output)
