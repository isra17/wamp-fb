from flask import abort
import registerer

_USERDB = {}

def handle_auth(user):
    global _USERDB
    _USERDB[user['id']] = {
        'secret': user['auth_token'],
        'role': 'user',
    }
    print(_USERDB)

def handle_wra(data):
    #IMPORTANT!: Request should be authenticated otherwise
    #anyone can dump anyone's auth token
    #DONT USE THIS SNIPPET IN PROD!
    print(data)
    authid = data['authid']
    if not authid in _USERDB:
        abort(401)
    return _USERDB[data['authid']]

app = registerer.create_app(handle_auth, handle_wra)
app.debug = True
app.run()
