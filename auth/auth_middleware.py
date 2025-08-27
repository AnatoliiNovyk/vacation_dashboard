def role_check_middleware(app):
    def middleware(environ, start_response):
        # Здесь можно сделать проверку cookie / session
        return app(environ, start_response)
    return middleware
