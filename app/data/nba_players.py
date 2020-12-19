import json

from datetime import datetime
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo


def generate_players_list():
    player_dict = players.get_players()
    playerz = len(player_dict)

    ballers = []
    for i in range(playerz):
        try:
            doc = {}
            baller = commonplayerinfo.CommonPlayerInfo(player_id=i).get_dict()['resultSets'][0]['rowSet'][0]
            doc['name'] = '{} {}'.format(baller[1], baller[2])
            doc['birth_date'] = datetime.strptime(baller[7].split('T')[0], "%Y-%m-%d")
            doc['nationality'] = baller[9]
            doc['height'] = baller[11]
            doc['weight'] = int(baller[12])
            doc['jersey'] = int(baller[14])
            doc['position'] = baller[15]
            doc['team'] = '{} {}'.format(baller[22], baller[19])
            doc['school'] = baller[8]
            doc['draft'] = {}
            doc['draft']['draft_year'] = int(baller[29])
            doc['draft']['draft_round'] = int(baller[30])
            doc['draft']['draft_number'] = int(baller[31])
            ballers.append(doc)
        except (json.decoder.JSONDecodeError, ValueError, TypeError):
            pass

    return ballers
