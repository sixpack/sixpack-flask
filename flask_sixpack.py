from datetime import timedelta

from flask import g, request

from sixpack import sixpack

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class Sixpack(object):

    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        app.config.setdefault('SIXPACK_HOST', 'http://localhost:5000')
        app.config.setdefault('SIXPACK_TIMEOUT', 0.5)
        app.config.setdefault('SIXPACK_COOKIE_NAME', 'sixpack_client_id')
        app.config.setdefault('SIXPACK_COOKIE_TIMEOUT', timedelta(days=365))

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

        app.after_request(self._after_request)

    def create_session(self):
        options = {
            'host': self.app.config['SIXPACK_HOST'],
            'timeout': self.app.config['SIXPACK_TIMEOUT']
        }
        params = {
            'user_agent': request.headers.get('User-Agent'),
            'ip_address': request.remote_addr
        }

        client_id = request.cookies.get(self.app.config['SIXPACK_COOKIE_NAME'], None)
        if (client_id is None):
            client_id = sixpack.generate_client_id()
            setattr(g, self.app.config['SIXPACK_COOKIE_NAME'], client_id)

        return sixpack.Session(client_id=client_id, options=options, params=params)

    def _after_request(self, response):
        if getattr(g, self.app.config['SIXPACK_COOKIE_NAME'], None) is None:
            return response

        response.set_cookie(self.app.config['SIXPACK_COOKIE_NAME'],
                            getattr(g, self.app.config['SIXPACK_COOKIE_NAME']),
                            max_age=self.app.config['SIXPACK_COOKIE_TIMEOUT'])
        response.vary.add('Cookie')
        return response

    def teardown(self, exception):
        pass

    @property
    def session(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'sixpack_session'):
                ctx.sixpack_session = self.create_session()
            return ctx.sixpack_session
