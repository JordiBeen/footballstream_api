import logging

from pyramid.view import view_config

log = logging.getLogger(__name__)


@view_config(route_name='general.entry_points', permission='public',
             renderer="json")
def general_entry_points(request):
    return {
        'entry_points': {
            'users': {
                'list': '/users',
                'get': '/users/{user_id}'
            },
            'competitions': {
                'list': '/competitions',
                'get': '/competitions/{competition_id}'
            },
            'standings': {
                'list': '/standings',
                'get': '/standings/{standing_id}'
            },
            'matches': {
                'list': '/matches',
                'get': '/matches/{match_id}',
                'list_current': '/matches/current',
                'list_finished': '/matches/finished',
                'list_by_team': '/matches?team_id={team_id} '
                                '(List of ids is allowed)'
            },
            'commentaries': {
                'list': '/commentaries',
                'get': '/commentaries/{commentary_id}'
            },
            'teams': {
                'list': '/teams',
                'get': '/teams/{team_id}',
                'list_by_competition': '/teams?competition_id={competition_id}'
            },
            'tweets': {
                'list': '/tweets',
                'get': '/tweets/{team_id}',
                'list_by_match': '/tweets?match_id={match_id}'
            },
            'players': {
                'list': '/players',
                'get': '/players/{player_id}'
            },
            'events': {
                'list': '/events',
                'get': '/events/{event_id}'
            }
        }
    }
