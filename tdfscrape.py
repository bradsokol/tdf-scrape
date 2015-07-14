#! /usr/bin/env python

from datetime import datetime
import argparse
import re
import sys

from bs4 import BeautifulSoup
from tabulate import tabulate
import requests


PLAYERS = []

OVERALL_RESULT_RE = re.compile(
    r'^ *(?P<rank>[\d]+)[.] *[(](?P<previous_rank>[\d]+)[)]'
    ' *(?P<overall_points>[\d]+)[(](?P<stage_delta>[+-]?[\d]+),(?P<points_behind>[-]?[\d]+)[)] *(?P<name>.+)'
    '[(](?P<country>.+)[)]$')
STAGE_RESULT_RE = re.compile(
    r'^ *(?P<stage_rank>[\d]+)[.] *(?P<stage_points>[\d]+) (?P<name>.+) [(](?P<country>.*)[)]$')


def build_arg_parser():
    parser = argparse.ArgumentParser(description='Parses results from the Tour de France game at http://ifarm.nl/tdf.')
    parser.add_argument(
        '-d',
        '--date',
        type=int,
        default=int(datetime.now().strftime('%Y%m%d')),
        help='Date of stage to parse for results requests. Format is YYYYMMDD. Default is today.'
    )
    parser.add_argument(
        '-f',
        '--file',
        type=argparse.FileType('r'),
        default='players.txt',
        help='Name of file containing list of players in a pool. Default is players.txt.'
    )
    parser.add_argument(
        '-s',
        '--sort',
        choices=['pool_rank', 'rank', 'stage_rank'],
        default='rank',
        help='Sorts stage results by rank, stage_rank or pool_rank.'
    )
    parser.add_argument(
        '-y',
        '--year',
        type=int,
        default=datetime.now().year,
        help='Year of race to parse. Default is current year.'
    )

    parser.add_argument(
        'type',
        choices=['overall', 'stage', 'teams']
    )
    return parser


def print_overall(date, sort='rank'):
    rows = []
    for player in PLAYERS:
        response = requests.post(
            'http://ifarm.nl/cgi-bin/getlines.cgi',
            {
                'DATE': date.strftime('%Y%m%d'),
                'SEARCH': player,
            }
        )
        response.raise_for_status()

        html = BeautifulSoup(response.text, 'html.parser')
        text = html.pre.get_text().split('\n')
        stage_match = STAGE_RESULT_RE.match(text[2])
        overall_match = OVERALL_RESULT_RE.match(text[4])
        rows.append([
            0,
            stage_match.group('name'),
            int(overall_match.group('rank')),
            int(overall_match.group('previous_rank')),
            int(overall_match.group('previous_rank')) - int(overall_match.group('rank')),
            int(overall_match.group('overall_points')),
            int(overall_match.group('points_behind')),
            0
        ])

    rows.sort(key=lambda row: row[2])
    top = rows[0][5]
    for i, row in enumerate(rows):
        row[0] = i + 1
        row[7] = row[5] - top

    if sort == 'stage_rank':
        rows.sort(key=lambda row: row[2])
    elif sort == 'pool_rank':
        rows.sort(key=lambda row: row[0])

    print(tabulate(
        rows,
        headers=[
            'Pool Rank', 'Name', 'Rank', 'Prev. Rank', 'Rank Change', 'Points', 'Behind', 'Pool Behind'
        ]
    ))


def print_stage(date, sort='rank'):
    rows = []
    for player in PLAYERS:
        response = requests.post(
            'http://ifarm.nl/cgi-bin/getlines.cgi',
            {
                'DATE': date.strftime('%Y%m%d'),
                'SEARCH': player,
            }
        )
        response.raise_for_status()

        html = BeautifulSoup(response.text, 'html.parser')
        text = html.pre.get_text().split('\n')
        stage_match = STAGE_RESULT_RE.match(text[2])
        rows.append([
            0,
            stage_match.group('name'),
            int(stage_match.group('stage_rank')),
            int(stage_match.group('stage_points')),
            0
        ])

    rows.sort(key=lambda row: row[2])
    top = rows[0][3]
    for i, row in enumerate(rows):
        row[0] = i + 1
        row[4] = row[3] - top

    if sort == 'stage_rank':
        rows.sort(key=lambda row: row[2])
    elif sort == 'pool_rank':
        rows.sort(key=lambda row: row[0])

    print(tabulate(
        rows,
        headers=[
            'Pool Rank', 'Name', 'Stage Rank', 'Stage Points', 'Pool Behind'
        ]
    ))


def print_teams(year):
    for player in PLAYERS:
        response = requests.post(
            'http://ifarm.nl/cgi-bin/getpart.cgi',
            {
                'SEARCH': player,
                'YEAR': year,
            }
        )
        response.raise_for_status()

        html = BeautifulSoup(response.text, 'html.parser')
        print(html.pre.get_text())


def read_players(players_file):
    global PLAYERS
    PLAYERS = players_file.read().split('\n')
    for player in list(PLAYERS):
        if len(player.strip()) == 0:
            PLAYERS.remove(player)


if __name__ == '__main__':
    arg_parser = build_arg_parser()
    args = arg_parser.parse_args()

    read_players(args.file)

    if args.type == 'overall':
        try:
            date = datetime.strptime(str(args.date), '%Y%m%d')
        except ValueError:
            print('Invalid date for stage. Must be YYYYMMDD.', file=sys.stderr)
            sys.exit(1)
        print_overall(date, args.sort)
    elif args.type == 'stage':
        try:
            date = datetime.strptime(str(args.date), '%Y%m%d')
        except ValueError:
            print('Invalid date for stage. Must be YYYYMMDD.', file=sys.stderr)
            sys.exit(1)
        print_stage(date, args.sort)
    elif args.type == 'teams':
        if args.year is None:
            print('The year parameter is required.', file=sys.stderr)
            sys.exit(1)
        print_teams(args.year)
