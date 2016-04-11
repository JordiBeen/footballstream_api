import logging

from pyramid.view import view_config

from ..models.team import get_team, list_teams

log = logging.getLogger(__name__)


@view_config(route_name='teams.get', permission='public',
             renderer="json")
def teams_get(request):
    team_id = request.matchdict['team_id']
    team = get_team(id_=team_id)

    return {
        'team': team.to_json()
    }


@view_config(route_name='teams.list', permission='public',
             renderer="json")
def teams_list(request):
    teams = list_teams()

    return {
        'teams': [team.to_json() for team in teams]
    }
