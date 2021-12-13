# -*- coding: utf-8 -*-
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
    res = requests.post(URL, headers=headers, json=system_info)

