# -*- coding: utf-8 -*-
"""
Copyright © 2012-2020 OpsAny. All Rights Reserved.
"""  # noqa

import requests
import json

import settings
from config import APP_CODE, SECRET_KEY, BK_URL
from bastion.utils.constants import IP_PATTERN, PRIVATE_IP_PATTERN


class EsbApi(object):
    def __init__(self, token=None, access_token=None):
        self.token = token if token else None
        self.app_code = APP_CODE
        self.app_secret = SECRET_KEY
        self.url = BK_URL
        self.access_token = access_token
        self.headers = {
            "Cookie": "bk_token={}".format(self.token)
        }

    def get_username(self):
        API = "/api/c/compapi/v2/bk_login/get_user/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            end_data = end_data.get("data").get("bk_username")
        return end_data

    def get_all_users(self):
        API = "/api/c/compapi/v2/bk_login/get_all_users/"
        req = {
            "bk_app_code": APP_CODE,
            "bk_app_secret": SECRET_KEY,
            "bk_token": self.token,
        }
        URL = self.url + API
        res = requests.get(URL, params=req, headers=self.headers, verify=False)
        user_list = json.loads(res.content)["data"]
        return user_list

    def get_nav_and_collection(self):
        API = "/api/c/compapi/workbench/get_nav_and_collection/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        dt = {}
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        return dt

    def collection_nav(self, nav_id):
        API = "/api/c/compapi/workbench/post_collection/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "nav_id": nav_id
        }
        URL = self.url + API
        response = requests.post(url=URL, data=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            return end_data
        return None

    def get_user_message_info(self, current=1, pageSize=10):
        API = "/api/c/compapi/workbench/get_message_info/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "current": str(current),
            "pageSize": str(pageSize)
        }
        URL = self.url + API
        response = requests.post(url=URL, data=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            data = end_data.get("data")
            return data
        return None

    def get_user_info(self):
        API = "/api/c/compapi/v2/bk_login/get_user/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        dt = {}
        if end_data.get("result"):
            dt["phone"] = end_data.get("data").get("phone")
            dt["username"] = end_data.get("data").get("bk_username")
            dt["email"] = end_data.get("data").get("email")
            dt["ch_name"] = end_data.get("data").get("chname")
            dt["role"] = end_data.get("data").get("bk_role")
        return dt

    def get_user_menu(self):
        API = "/api/c/compapi/rbac/post_menu_tree/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "platform_cname": "bastion"
        }
        URL = self.url + API
        response = requests.post(url=URL, data=json.dumps(req), headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        # print("end_data", end_data)
        return end_data.get("data")

    def get_user_info_from_workbench(self):
        """从工作台ESB获取用户信息"""
        API = "/api/c/compapi/workbench/get_user_info_from_workbench/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
        }
        URL = self.url + API
        response = requests.post(url=URL, data=json.dumps(req), headers=self.headers, verify=False, timeout=2)
        end_data = json.loads(response.text)

        return end_data.get("data")

    def get_user_info_from_workbench_or_login(self):
        """首先获取工作台数据，获取不到再获取login数据"""
        try:
            end_data = self.get_user_info_from_workbench()
            if not end_data:
                raise Exception("workbench return None")
            # print("使用workbench信息")
        except Exception as e:
            # print("使用login信息")
            # print("get_user_info_from_workbench_or_login_error_workbench:", e)
            default_user_icon = getattr(settings, "DEFAULT_USER_ICON",
                                        "uploads/workbench/user_icon/edfb99ee-08d6-41b8-ac5f-117fb86b0912.png")
            end_data = self.get_user_info()
            if end_data and isinstance(end_data, dict):
                end_data['icon_url'] = default_user_icon
        return end_data

    def read_all_message(self):
        API = "/api/c/compapi/workbench/get_read_all_message/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        return end_data.get("data")

    def get_user_group_sync(self):
        API = "/api/c/compapi/rbac/get_user_group_sync/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token
        }
        if not self.token:
            req["bk_access_token"] = self.access_token
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        return {}

    def get_department_user_tree(self):
        API = "/api/c/compapi/rbac/get_department_user_tree/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        return end_data.get("data")

    def get_control_agent_info(self, system_type=None, group_type=None):
        API = "/api/c/compapi/control/get_control_agent_info/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            'token_data': self.token,
            'system_type': system_type,
            'group_type': group_type
        }
        URL = self.url + API
        response = requests.post(url=URL, data=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            data = end_data.get("data")
            agent_info = data[0].get("agent_info")
            for i in agent_info:
                ip = i.get("ip", "")
                if IP_PATTERN.match(ip):
                    ip_type = "(内)" if PRIVATE_IP_PATTERN.match(ip) else "(外)"
                    i["ip_type"] = ip_type
                else:
                    i["ip_type"] = "(不明)"
            end_data = end_data.get("data")
        return end_data

    def host_group_to_job(self, info, filter={}):
        API = "/api/c/compapi/control/host_group_to_job/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "group_list": info,
            "filters": filter
        }
        if not self.token:
            req["bk_access_token"] = self.access_token
        URL = self.url + API
        req = json.dumps(req)
        response = requests.post(url=URL, data=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("data"):
            return end_data.get("data")
        return []

    def host_admin_from_group_to_job(self, group_id):
        API = "/api/c/compapi/control/host_admin_from_group_to_job/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "token_data": self.token,  # 用于获取当前用户
            "group_id": group_id,
        }
        if not self.token:
            req["bk_access_token"] = self.access_token
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("data"):
            return end_data.get("data")
        return []

    def run_script(self, host_list, script_url, arg):
        "https://dev.opsany.cn/api/c/compapi/control/get_request_id_status/"
        API = "/api/c/compapi/control/post_script/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "host_list": host_list,  # [unique1, unique2, unique3]
            "script_url": script_url,
            "arg": arg,
        }
        if not self.token:
            req["bk_access_token"] = self.access_token
        print(req)
        URL = self.url + API
        response = requests.post(url=URL, json=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        print(end_data)
        if end_data.get("data"):
            return end_data.get("data")
        return ""

    def get_request_id_status(self, request_id):
        API = "/api/c/compapi/control/get_request_id_status/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "request_id": request_id
        }
        if not self.token:
            req["bk_access_token"] = self.access_token
        print(req)
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        print(end_data)
        if end_data.get("data"):
            return end_data.get("data")
        return []

    def get_user_ssh_key(self, ssh_key_id=""):
        API = "/api/c/compapi/workbench/get_user_ssh_key/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "ssh_key_id": ssh_key_id,
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        return end_data.get("data")

    def get_all_host(self, search_type=None, search_data=None):
        API = "/api/c/compapi/cmdb/get_all_host/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "model_code": "esb",
            "search_type": search_type,
            "search_data": search_data,
        }
        print(req)
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        # print(end_data)
        end_data = end_data.get("data")
        return end_data

    def list_departments(self):
        """
        带分页
        "page_size": 1,
        "page": 2
        """
        API = "/api/c/compapi/v2/usermanage/list_departments/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("data"):
            return end_data.get("data")
        return []

    def list_department_profiles(self):
        API = "/api/c/compapi/v2/usermanage/list_department_profiles/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("data"):
            return end_data.get("data")
        return []

    def list_users(self, page, page_size, lookup_field="", fuzzy_lookups=""):
        API = "/api/c/compapi/v2/usermanage/list_users/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "page": page if page else 1,
            "page_size": page_size if page_size else 10,
            "lookup_field": lookup_field,
            "fuzzy_lookups": fuzzy_lookups
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("data"):
            return end_data.get("data")
        return {}

    def retrieve_user(self, username):
        API = "/api/c/compapi/v2/usermanage/retrieve_user/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "id": username
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("data"):
            return end_data.get("data")
        return {}


if __name__ == '__main__':
    # esb = EsbApi("m421zYp6i5v8vOjD-_E8gAzNZ4tSOtmgsE7LWkbEbt8")
    # esb = EsbApi("LilyG11EWaKBPTOF1ntULcXrkpK4IIu4v_K2eHOlcYg")
    # esb = EsbApi("0B1S4K4o8g2sgYSXXDWDwPrSrWec4Bizv2K73l7t76Y")
    esb = EsbApi("TRrWFNe1dCrhmDWv4upSuqmd9vn5wYDWMslj9dYF_9o")
    print(esb.get_user_info())
    # print(esb.retrieve_user("demo01"))
    # print(esb.get_user_info())

