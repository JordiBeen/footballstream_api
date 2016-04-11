import logging

from pyramid.view import view_config

from ..models.match import get_match, list_matches

log = logging.getLogger(__name__)


@view_config(route_name='matches.get', permission='public',
             renderer="json")
def matches_get(request):
    match_id = request.matchdict['match_id']
    match = get_match(id_=match_id)

    return {
        'match': match.to_json()
    }


@view_config(route_name='matches.list', permission='public',
             renderer="json")
def matches_list(request):
    matches = list_matches()

    return {
        'matches': [match.to_json() for match in matches]
    }
