import sys
import pymysql
import argparse
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AddUser:
    def __init__(self, bk_url, bk_username, bk_password, app_code, app_token):
        self.session = requests.Session()
        self.url = bk_url
        self.bk_username = bk_username
        self.bk_password = bk_password
        self.app_code = app_code
        self.app_token = app_token
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
            'username': self.bk_username,
            'password': self.bk_password
        }
        resp = self.session.post(URL, data=login_form, verify=False)

        if resp.status_code == 200:
            if resp.cookies.get("sessionid"):
                return True
            else:
                return False
        else:
            return False

    def get_user_list(self):
        if not self.login_status:
            print("[Error] Get bk token error, please check your url, bk_username, bk_password.")
            return []
        API = "/api/c/compapi/v2/usermanage/list_users/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_token,
            "bk_token": self.session.cookies.get("bk_token"),
            "page_size": 100,
        }
        page = 0
        URL = self.url + API
        user_list = []
        while True:
            page += 1
            req["page"] = page
            response = requests.get(url=URL, params=req, headers=self.session.headers, verify=False)
            end_data = response.json()
            if end_data.get("data"):
                user_list.extend(end_data.get("data").get("results"))
            else:
                break
        return [
            {
                "username": user.get("username"),
                "ch_name": user.get("display_name"),
                "email": user.get("email"),
                "phone": user.get("telephone"),
                "role": user.get("role")
            }
            for user in user_list]

    def retrieve_user(self, username):
        API = "/api/c/compapi/v2/usermanage/retrieve_user/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_token,
            "bk_token": self.session.cookies.get("bk_token"),
            "id": username
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.session.headers, verify=False)
        end_data = response.json()
        if end_data.get("data"):
            return end_data.get("data")
        return {}


class AutoAddUserToAccess:
    def __init__(self, db_host, db_port, db_user, db_password, database, access_names,
                 bk_url, bk_username, bk_password, app_code, app_token):
        try:
            self.db = pymysql.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=database
            )
        except Exception as e:
            print("[ERROR] Create database link error: {}".format(str(e)))
            sys.exit(1)
        self.access_names = access_names
        self.user_component = AddUser(bk_url, bk_username, bk_password, app_code, app_token)
        if not self.user_component.login_status:
            print("[Error] Get bk token error, please check your url, bk_username, bk_password.")
            sys.exit(1)
        self.user_list = self.user_component.get_user_list()

    def fetch_all(self, sql):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            print("Fetch all error: {}, param: {}".format(str(e), sql))
            return ()

    def get_user(self):
        sql = """
        SELECT * FROM user_info;
        """
        res = self.fetch_all(sql)
        return [_res[0] for _res in res if _res[0]]

    def get_access_id(self, access_name):
        sql = """
        SELECT * FROM strategy_access where NAME='{}'
        """.format(access_name)
        res = self.fetch_all(sql)
        if res:
            return res[0][0]
        else:
            return None

    def get_access_user(self, access_id):
        sql = """
        SELECT * FROM strategy_access_user_group_relationship WHERE strategy_access_id={}
        """.format(access_id)
        res = self.fetch_all(sql)
        return [_res[4] for _res in res if _res[4]]

    def insert(self, sql):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print("Insert data error: {}, param: {}".format(str(e), sql))
            return False

    def add_user_to_access(self, user_id, access_id):
        sql = """
        INSERT INTO strategy_access_user_group_relationship (create_time, update_time, user_id, strategy_access_id) VALUES (NOW(), NOW(), {}, {}); 
        """.format(user_id, access_id)
        res = self.insert(sql)
        if res:
            print("Create success.")
        else:
            print("Create error.")

    def _auto_add(self, access_id, user_list):
        access_user = self.get_access_user(access_id)
        for user_id in user_list:
            if user_id not in access_user:
                self.add_user_to_access(user_id, access_id)

    def auto_add_user_to_bastion(self):
        for user in self.user_list:
            sql = """
            SELECT * FROM user_info where username="{}"
            """.format(user.get("username"))
            res = self.fetch_all(sql)
            if not res:
                user_info = self.user_component.retrieve_user(user.get("username"))
                if user_info and user.get("username"):
                    create_sql = """
                    INSERT INTO user_info (create_time, update_time, phone, username, email, ch_name, role) 
                    VALUES (NOW(), NOW(), '{}', '{}', '{}', '{}', '{}');
                    """.format(
                        user_info.get("telephone", ""),
                        user_info.get("username"),
                        user_info.get("email", ""),
                        user_info.get("display_name", ""),
                        user_info.get("role", "")
                    )
                    self.insert(create_sql)
                else:
                    print("[ERROR] Create user error, param: {}".format(user))

    def auto_add_user_to_access(self):
        user_list = self.get_user()
        for access_name in self.access_names:
            access_id = self.get_access_id(access_name)
            if not access_id:
                print("Not find access, access name: {}".format(access_name))
                continue
            else:
                self._auto_add(access_id, user_list)

    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def run(self):
        self.auto_add_user_to_bastion()
        self.auto_add_user_to_access()


def add_parameter():
    parameter = argparse.ArgumentParser()
    parameter.add_argument("--db_host", help="Required parameters.", required=True)
    parameter.add_argument("--db_port", help="Required parameters.", required=True, type=int)
    parameter.add_argument("--db_user", help="Required parameters.", required=True)
    parameter.add_argument("--db_password", help="Required parameters.", required=True)
    parameter.add_argument("--database", help="Required parameters.", required=True)
    parameter.add_argument("--access_names", help="Required parameters.", required=True, nargs="+")
    parameter.add_argument("--bk_url", help="Required parameters.", required=True)
    parameter.add_argument("--bk_username", help="Required parameters.", required=True)
    parameter.add_argument("--bk_password", help="Required parameters.", required=True)
    parameter.add_argument("--app_code", help="Required parameters.", required=True)
    parameter.add_argument("--app_token", help="Required parameters.", required=True)
    parameter.parse_args()
    return parameter


if __name__ == '__main__':
    parameter = add_parameter()
    options = parameter.parse_args()
    db_host = options.db_host
    db_port = options.db_port
    db_user = options.db_user
    db_password = options.db_password
    database = options.database
    access_names = options.access_names
    bk_url = options.bk_url
    bk_username = options.bk_username
    bk_password = options.bk_password
    app_code = options.app_code
    app_token = options.app_token
    AutoAddUserToAccess(
        db_host, db_port, db_user, db_password, database, access_names,
        bk_url, bk_username, bk_password, app_code, app_token
    ).run()
