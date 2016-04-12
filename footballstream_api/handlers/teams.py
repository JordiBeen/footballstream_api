import logging

from pyramid.view import view_config

from ..models.competition import get_competition
from ..models.team import get_team, list_teams

log = logging.getLogger(__name__)


@view_config(route_name='teams.get', permission='public',
             renderer="json")
def teams_get(request):
    team_id = request.matchdict['team_id']
    team = get_team(id_=team_id)

    return {
        'team': team.to_json_detail()
    }


@view_config(route_name='teams.list', permission='public',
             renderer="json")
def teams_list(request):
    competition_id = request.params.get('competition_id')
    teams = list_teams()

    if competition_id:
        competition_teams = []
        competition = get_competition(id_=competition_id)
        for team in teams:
            if competition in team.competitions:
                competition_teams.append(team)

        teams = competition_teams

    return {
        'teams': [team.to_json() for team in teams]
    }
