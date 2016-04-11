import logging

from pyramid.view import view_config

from ..models.user import get_user, list_users

log = logging.getLogger(__name__)


@view_config(route_name='users.get', permission='public',
             renderer="json")
def users_get(request):
    user_id = request.matchdict['user_id']
    user = get_user(id_=user_id)

    return {
        'user': user.to_json()
    }


@view_config(route_name='users.list', permission='public',
             renderer="json")
def users_list(request):
    users = list_users()

    return {
        'users': [user.to_json() for user in users]
    }
