import logging

from pyramid.view import view_config

from ..models.match import get_match, list_matches
from ..models.team import get_team

log = logging.getLogger(__name__)


@view_config(route_name='matches.get', permission='public',
             renderer="json")
def matches_get(request):
    match_id = request.matchdict['match_id']
    match = get_match(id_=match_id)

    return {
        'match': match.to_json_detail()
    }


@view_config(route_name='matches.list', permission='public',
             renderer="json")
def matches_list(request):
    team_id = request.params.get('team_id')
    matches = list_matches()

    # If there are team_ids given as param
    if team_id:
        team_matches = []
        for id in team_id.split(','):
            team = get_team(id_=id)
            for match in matches:
                if match.localteam is team or match.visitorteam is team:
                    team_matches.append(match)
        matches = team_matches

    return {
        'matches': [match.to_json() for match in matches]
    }
