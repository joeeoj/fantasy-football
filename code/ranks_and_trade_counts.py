import requests


url = ('https://fantasy.espn.com/apis/v3/games/ffl/seasons/2021/segments/0/leagues/17588244?'
       'view=mPendingTransactions&view=mSettings&view=mStatus'
       '&view=mMatchupScore&view=mTeam&view=modular&view=mNav')
r = requests.get(url)

data = r.json()
teams = data.get('teams')


for team in teams:
    wavier_rank = team.get('waiverRank')
    draft_day_rank = team.get('draftDayProjectedRank')
    current_projected_rank = team.get('currentProjectedRank')

    rank = team.get('rankFinal')
    rank_calc = team.get('rankCalculatedFinal')

    name = ' '.join([team.get('location'), team.get('nickname')])
    
    transaction_counter = team.get('transactionCounter')
    trade_block = team.get('tradeBlock')

    print(name)
    # for k,v in transaction_counter.items():
    #     print(f'{k}: {v}')
    # print('-' * 80)
