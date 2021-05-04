import requests
import os
from requests.auth import HTTPBasicAuth


def make_getter():
    HOST = os.environ.get("TEAMCITY_HOST")
    USER = os.environ.get("TEAMCITY_USER")
    PWD = os.environ.get("TEAMCITY_PWD")
    auth = HTTPBasicAuth(USER, PWD)

    def get(path=None, href=None, to_json=True):
        assert path or href
        if path:
            r = requests.get(f"{HOST}/app/rest/{path}", auth=auth, headers={"accept": "application/json"})
        else:
            r = requests.get(f"{HOST}{href}", auth=auth, headers={"accept": "application/json"})
        return r.json() if to_json else r

    return get


get = make_getter()
