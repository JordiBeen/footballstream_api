import logging

from pyramid.view import view_config

from ..models.user import get_user, list_users

log = logging.getLogger(__name__)


@view_config(route_name='general.entry_points', permission='public',
             renderer="json")
def general_entry_points(request):
    return {
        'entry_points': {
            'users.list': '/api/v1/users',
            'users.get': '/api/v1/users/{user_id}'
        }
    }
