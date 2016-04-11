import logging

from pyramid.view import view_config

from ..models.competition import get_competition, list_competitions

log = logging.getLogger(__name__)


@view_config(route_name='competitions.get', permission='public',
             renderer="json")
def competitions_get(request):
    competition_id = request.matchdict['competition_id']
    competition = get_competition(id_=competition_id)

    return {
        'competition': competition.to_json()
    }


@view_config(route_name='competitions.list', permission='public',
             renderer="json")
def competitions_list(request):
    competitions = list_competitions()

    return {
        'competitions': [competition.to_json() for competition in competitions]
    }
