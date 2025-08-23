def role_check_middleware(app):
    def middleware(environ, start_response):
        # Базова перевірка middleware
        return app(environ, start_response)
    return middleware
