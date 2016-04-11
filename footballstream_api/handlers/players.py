import logging

from pyramid.view import view_config

from ..models.player import get_player, list_players

log = logging.getLogger(__name__)


@view_config(route_name='players.get', permission='public',
             renderer="json")
def players_get(request):
    player_id = request.matchdict['player_id']
    player = get_player(id_=player_id)

    return {
        'player': player.to_json()
    }


@view_config(route_name='players.list', permission='public',
             renderer="json")
def players_list(request):
    players = list_players()

    return {
        'players': [player.to_json() for player in players]
    }
