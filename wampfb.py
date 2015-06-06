import cgi
import urllib
import json
from urllib import request
from urllib.error import URLError

status = {
    401: '401 Unauthorized',
    404: '404 Not Found',
    422: '422 Unprocessable Entity',
}

def is_auth_request(environ):
    return environ['REQUEST_METHOD'] != 'POST' and environ['PATH_INFO'] != '/auth'

def get_post(environ):
    post_env = environ.copy()
    post_env['QUERY_STRING'] = ''
    post = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=post_env
    )
    return post

def fb_user(fb_token, fields=[]):
    url = 'https://graph.facebook.com/v2.3/me?' \
            + 'fields=' + request.quote(','.join(fields)) \
            + '&access_token=' + request.quote(fb_token)
    try:
        r = request.urlopen(url)
        return json.loads(r.read().decode())
    except URLError as e:
        return None

def create_app(auth_handler, user_fields=[]):
    def app(environ, response):
        if is_auth_request(environ):
            response(status[404], [])
            return ''

        post = get_post(environ)
        if not 'fb_token' in post:
            response(status[422], [])
            return ''
        fb_token = post['fb_token'].value

        user_data = fb_user(fb_token, user_fields)
        if user_data is None:
            response(status[401], [])
            return ''

        return auth_handler(user_data, environ, response)

    return app
