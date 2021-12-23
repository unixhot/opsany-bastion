# -*- coding: utf-8 -*-
import requests
from config import APP_CODE, SECRET_KEY
import os


def init_system_to_iam():
    system_info = {
        "id": os.getenv("APP_ID", APP_CODE),
        "name": "OpsAny堡垒机",
        "name_en": "bastion",
        "description": "堡垒机",
        "description_en": "bastion iam",
        "clients": "bastion,",
        "provider_config": {
            "host": "{}/o/bastion/".format("BK_PAAS_HOST"),
            "auth": "basic",
            "healthz": "/test/"
        }
    }
    # 必须是内网
    IAM_HOST = os.getenv("BK_IAM_V3_INNER_HOST", "http://bkiam.service.consul:5001")
    API = "/api/v1/model/systems/"
    URL = IAM_HOST + API
    headers = {
        "X-Bk-App-Code": APP_CODE,
        "X-Bk-App-Secret": SECRET_KEY,
        "Content-Type": "application/json"
    }
    res = requests.post(URL, headers=headers, json=system_info)
    print(res.json())

