import requests


def init_system_to_iam():
    system_info = {
        "id": "bastion-blueking",
        "name": "堡垒机IAM测试",
        "name_en": "bastion-blueking",
        "description": "堡垒机IAM测试",
        "description_en": "bastion iam test",
        "clients": "bastion-blueking,",
        "provider_config": {
            "host": "http://paas.opsany.com/t/bastion-blueking/",
            "auth": "basic",
            "healthz": "/test/"
        }
    }
    # 必须是内网
    IAM_HOST = "http://bkiam.service.consul:5001"
    APP_CODE = "bastion-blueking"
    SECRET_KEY = "4f49d205-87fc-4137-a446-27ab878bfa4c"
    API = "/api/v1/model/systems/"
    URL = IAM_HOST + API
    # A = "http://paas.opsany.com/bk_iam"
    # URL = A + API
    headers = {
        "X-Bk-App-Code": APP_CODE,
        "X-Bk-App-Secret": SECRET_KEY,
        "Content-Type": "application/json"
    }
    print(URL)
    res = requests.post(URL, headers=headers, json=system_info)
    print(res)
    print(res.text)


def add_action_to_system():
    actions = [
        {
            "id": "visit-host-resources",
            "name": "访问主机资源",
            "name_en": "visit host resources",
            "description": "访问主机资源",
            "description_en": "visit host resources",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        },
    ]
    # 必须是内网
    IAM_HOST = "http://bkiam.service.consul:5001"
    APP_CODE = "bastion-blueking"
    SECRET_KEY = "4f49d205-87fc-4137-a446-27ab878bfa4c"
    API = "/api/v1/model/systems/{system_id}/actions".format(system_id=APP_CODE)
    URL = IAM_HOST + API
    # A = "http://paas.opsany.com/bk_iam"
    # URL = A + API
    headers = {
        "X-Bk-App-Code": APP_CODE,
        "X-Bk-App-Secret": SECRET_KEY,
        "Content-Type": "application/json"
    }
    print(URL)
    res = requests.post(URL, headers=headers, json=actions)
    print(res)
    print(res.text)


# if __name__ == '__main__':
#     import os
#     import sys
#     import requests
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
#     import datetime
#
#     print(" [Success] {} init iam Running".format(str(datetime.datetime.now()).rsplit(".", 1)[0]))
#     # os.environ["BK_ENV"] = os.getenv("BK_ENV", "production")
#     # os.environ.setdefault("BK_ENV", "production")     # 生产环境解注改行
#     # os.environ.setdefault("BK_ENV", "testing")        # 开发环境解注改行
#     sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
#     import django
#     import settings
#     django.setup()
#     init_system_to_iam()
#     print(" [Success] {} init iam Execution Complete".format(str(datetime.datetime.now()).rsplit(".", 1)[0]))
