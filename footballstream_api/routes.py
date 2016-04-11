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

    ###
    # COMPETITIONS
    ###
    # LIST
    config.add_route('competitions.list', '/api/v1/competitions')
    # GET
    config.add_route('competitions.get', '/api/v1/competitions/\
        {competition_id}')

    ###
    # STANDINGS
    ###
    # LIST
    config.add_route('standings.list', '/api/v1/standings')
    # GET
    config.add_route('standings.get', '/api/v1/standings/{standing_id}')

    ###
    # MATCHES
    ###
    # LIST
    config.add_route('matches.list', '/api/v1/matches')
    # GET
    config.add_route('matches.get', '/api/v1/matches/{match_id}')

    ###
    # COMMENTARIES
    ###
    # LIST
    config.add_route('commentaries.list', '/api/v1/commentaries')
    # GET
    config.add_route('commentaries.get', '/api/v1/commentaries/\
            {commentary_id}')

    ###
    # TEAMS
    ###
    # LIST
    config.add_route('teams.list', '/api/v1/teams')
    # GET
    config.add_route('teams.get', '/api/v1/teams/{team_id}')

    ###
    # PLAYERS
    ###
    # LIST
    config.add_route('players.list', '/api/v1/players')
    # GET
    config.add_route('players.get', '/api/v1/players/{player_id}')
