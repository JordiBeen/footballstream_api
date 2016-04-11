import logging

from pyramid.view import view_config

log = logging.getLogger(__name__)


@view_config(route_name='general.entry_points', permission='public',
             renderer="json")
def general_entry_points(request):
    return {
        'entry_points': {
            'users': {
                'list': '/api/v1/users',
                'get': '/api/v1/users/{user_id}'
            },
            'competitions': {
                'list': '/api/v1/competitions',
                'get': '/api/v1/competitions/{competition_id}'
            },
            'standings': {
                'list': '/api/v1/standings',
                'get': '/api/v1/standings/{standing_id}'
            },
            'matches': {
                'list': '/api/v1/matches',
                'get': '/api/v1/matches/{match_id}'
            },
            'commentaries': {
                'list': '/api/v1/commentaries',
                'get': '/api/v1/commentaries/{commentary_id}'
            },
            'teams': {
                'list': '/api/v1/teams',
                'get': '/api/v1/teams/{team_id}'
            },
            'players': {
                'list': '/api/v1/players',
                'get': '/api/v1/players/{player_id}'
            },
            'events': {
                'list': '/api/v1/events',
                'get': '/api/v1/events/{event_id}'
            }
        }
    }
