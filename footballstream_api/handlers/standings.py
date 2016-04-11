import logging

from pyramid.view import view_config

from ..models.standing import get_standing, list_standings

log = logging.getLogger(__name__)


@view_config(route_name='standings.get', permission='public',
             renderer="json")
def standings_get(request):
    standing_id = request.matchdict['standing_id']
    standing = get_standing(id_=standing_id)

    return {
        'standing': standing.to_json()
    }


@view_config(route_name='standings.list', permission='public',
             renderer="json")
def standings_list(request):
    standings = list_standings()

    return {
        'standings': [standing.to_json() for standing in standings]
    }
