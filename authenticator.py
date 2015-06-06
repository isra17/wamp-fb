from os import environ
import requests
import urlparse

auth_server = urlparse.urljoin(environ['AUTH_SERVER'], 'wra')
def authenticate(realm, authid, details):
    params = urllib2.urlencode({realm: realm, authid: authid, details: details})
    r = requests.post(auth_server, data=params)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception('authenticate error: {}'.format(r.reason))

