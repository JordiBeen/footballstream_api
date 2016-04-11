import logging

from pyramid.view import view_config

from ..models.event import get_event, list_events

log = logging.getLogger(__name__)


@view_config(route_name='events.get', permission='public',
             renderer="json")
def events_get(request):
    event_id = request.matchdict['event_id']
    event = get_event(id_=event_id)

    return {
        'event': event.to_json_detail()
    }


@view_config(route_name='events.list', permission='public',
             renderer="json")
def events_list(request):
    events = list_events()

    return {
        'events': [event.to_json() for event in events]
    }
