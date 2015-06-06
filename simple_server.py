from wsgiref.simple_server import make_server
import wampfb
import json

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def auth_handler(user, environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json; charset=utf-8')]

    start_response(status, headers)

    return [json.dumps(user).encode()]

httpd = make_server('', 8000, wampfb.create_app(auth_handler))
print("Serving on port 8000...")
httpd.serve_forever()
