from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .routes import setup_routes
from .models.meta import DBSession, Base
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.events import NewRequest


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
                          session_factory=my_session_factory)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)

    setup_routes(config)
    config.scan()
    return config.make_wsgi_app()
