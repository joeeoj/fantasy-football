#!/usr/bin/env python3
"""Download and parse NFL depth charts from the Huddle"""
from typing import List

import bs4
from bs4 import BeautifulSoup
import requests


URL = 'https://tools.thehuddle.com/nfl-depth-charts'
LEGEND {
    '(N)': 'New to Team',
    '(R)': 'Rookie',
    '(IR)': 'Injured Reserve',
    '(PUP)': 'Physically Unable to Perform',
    '(IR-R)': 'Injured Reserve w/ opportunity to return',
    '(SUS)': 'Suspended',
}

def parse_qualifier(val: str) -> str:
    for k,v in LEGEND.items():
        if k in 


r = requests.get(URL)
soup = BeautifulSoup(r.content, 'lxml')
table = soup.find_all(attrs={'data-reactid': 314})
rows = soup.find_all('tr')
header = [item.text for item in rows[0].find_all('th')]


def parse_row(row: bs4.element.Tag) -> List[List[str]]:
    results = []
    for col in row.find_all('td'):
        col_results = []
        for item in col.find_all('a'):
            val = item.text.strip()
            if 
            col_results.append(item.text.strip())
        results.append(col_results)
    return results

# TODO - finish this...maybe
test = rows[1]
items = parse_row(test)
