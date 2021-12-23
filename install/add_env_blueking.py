import requests
import argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BkApi(object):
    def __init__(self, username, password, paas_url):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.url = paas_url
        self.session.verify = False
        self.session.headers.update({'referer': self.url})
        self.csrfmiddlewaretoken = self.get_csrftoken()
        self.login_status = self.login()

    def get_csrftoken(self):
        API = "/login/"
        URL = self.url + API
        resp = self.session.get(URL, verify=False)
        if resp.status_code == 200:
            return resp.cookies["bklogin_csrftoken"]
        return None

    def login(self):
        API = "/login/"
        URL = self.url + API
        login_form = {
            'csrfmiddlewaretoken': self.csrfmiddlewaretoken,
            'username': self.username,
            'password': self.password
        }
        resp = self.session.post(URL, data=login_form, verify=False)
        if resp.status_code == 200:
            if resp.cookies.get("sessionid"):
                return True
            else:
                return False
        else:
            return False

    def add_env(self, app_code, envs):
        if self.login_status:
            URL = self.url + "/app/env/{}/add/".format(app_code)
            for env in envs:
                resp = self.session.post(URL, data=env, headers={"X-CSRFToken": self.session.cookies.get("bk_csrftoken")})
                if resp.status_code == 200:
                    print("Env {} add success".format(env.get("name")))
                else:
                    print("Env {} add error".format(env.get("name")))
        else:
            print("Login failed, check your username or password, pleases.")


def get_params(app_code="", mysql_password="", mysql_host="", mysql_port="", redis_host="", redis_port="", redis_password=""):
    APP_CODE = app_code
    ENV_INFO = [
        {"name": "MYSQL_PASSWORD", "value": mysql_password, "intro": "mysql password", "mode": "all"},
        {"name": "MYSQL_HOST", "value": mysql_host, "intro": "mysql host", "mode": "all"},
        {"name": "MYSQL_PORT", "value": mysql_port, "intro": "mysql port", "mode": "all"},
        {"name": "REDIS_HOST", "value": redis_host, "intro": "redis host", "mode": "all"},
        {"name": "REDIS_PORT", "value": redis_port, "intro": "redis port", "mode": "all"},
        {"name": "REDIS_PASSWORD", "value": redis_password, "intro": "redis password", "mode": "all"},
    ]
    return APP_CODE, ENV_INFO


def add_parameter():
    parameter = argparse.ArgumentParser()
    parameter.add_argument("--username", help="Paas admin username.", required=True)
    parameter.add_argument("--password", help="Paas admin password.", required=True)
    parameter.add_argument("--paas_url", help="Paas url.", required=True)
    parameter.add_argument("--app_code", help="App code.", required=False)
    parameter.add_argument("--mysql_password", help="Mysql password.", required=False)
    parameter.add_argument("--mysql_host", help="Mysql host.", required=False)
    parameter.add_argument("--mysql_port", help="Mysql port.", required=False)
    parameter.add_argument("--redis_host", help="Redis host.", required=False)
    parameter.add_argument("--redis_port", help="Redis port.", required=False)
    parameter.add_argument("--redis_password", help="Redis password.", required=False)
    return parameter


if __name__ == '__main__':
    DEFAULT_APP_CODE = "bastion"
    DEFAULT_MYSQL_PASSWORD = "1"
    DEFAULT_MYSQL_HOST = "2"
    DEFAULT_MYSQL_PORT = "3"
    DEFAULT_REDIS_HOST = "4"
    DEFAULT_REDIS_PORT = "5"
    DEFAULT_REDIS_PASSWORD = "6"
    parameter = add_parameter()
    options = parameter.parse_args()
    username = options.username
    password = options.password
    paas_url = options.paas_url
    app_code = DEFAULT_APP_CODE if not options.app_code else options.app_code
    mysql_password = DEFAULT_MYSQL_PASSWORD if not options.mysql_password else options.mysql_password
    mysql_host = DEFAULT_MYSQL_HOST if not options.mysql_host else options.mysql_host
    mysql_port = DEFAULT_MYSQL_PORT if not options.mysql_port else options.mysql_port
    redis_host = DEFAULT_REDIS_HOST if not options.redis_host else options.redis_host
    redis_port = DEFAULT_REDIS_PORT if not options.redis_port else options.redis_port
    redis_password = DEFAULT_REDIS_PASSWORD if not options.redis_password else options.redis_password
    bk_api = BkApi(username, password, paas_url)
    app_code, envs = get_params(app_code, mysql_password, mysql_host, mysql_port, redis_host, redis_port, redis_password)
    bk_api.add_env(app_code, envs)

