from flask import Flask, request, abort
import urllib
import json

def fb_user(fb_token, fields=[]):
    url = 'https://graph.facebook.com/v2.3/me?' \
            + 'fields=' + urllib.request.quote(','.join(fields)) \
            + '&access_token=' + urllib.request.quote(fb_token)
    try:
        r = urllib.request.urlopen(url)
        return json.loads(r.read().decode())
    except urllib.error.URLError as e:
        return None

def create_app(handle_auth, wra_info, user_fields=[]):
    app = Flask(__name__)

    @app.route('/auth', methods=['POST'])
    def auth():
        fb_token = request.form['fb_token']
        if fb_token is None:
            abort(401)

        user_data = fb_user(fb_token, user_fields)
        if user_data is None:
            abort(401)

        user_data['auth_token'] = fb_token
        if handle_auth(user_data) == False:
            abort(401)

        return ''

    @app.route('/wra', methods=['POST'])
    def wra():
        #IMPORTANT!: Request should be authenticated otherwise
        #anyone can dump anyone's auth token
        return json.dumps(wra_info(request.form))

    return app

