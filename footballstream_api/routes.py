def setup_routes(config):

    ###
    # ENTRY POINTS
    ###
    config.add_route('general.entry_points', '/api/v1')

    ###
    # USERS
    ###
    # LIST
    config.add_route('users.list', '/api/v1/users')
    # GET
    config.add_route('users.get', '/api/v1/users/{user_id}')
