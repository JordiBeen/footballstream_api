import logging

from pyramid.view import view_config

from ..models.commentary import get_commentary, list_commentaries

log = logging.getLogger(__name__)


@view_config(route_name='commentaries.get', permission='public',
             renderer="json")
def commentaries_get(request):
    commentary_id = request.matchdict['commentary_id']
    commentary = get_commentary(id_=commentary_id)

    return {
        'commentary': commentary.to_json()
    }


@view_config(route_name='commentaries.list', permission='public',
             renderer="json")
def commentaries_list(request):
    commentaries = list_commentaries()

    return {
        'commentaries': [commentary.to_json() for commentary in commentaries]
    }
