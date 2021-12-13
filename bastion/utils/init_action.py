# -*- coding: utf-8 -*-
import requests
import os


def add_action_to_system():
    IAM_HOST = os.getenv("BK_IAM_V3_INNER_HOST", "http://bkiam.service.consul:5001")
    APP_CODE = os.getenv("APP_ID")
    SECRET_KEY = os.getenv("APP_TOKEN")
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
    API = "/api/v1/model/systems/{system_id}/actions".format(system_id=APP_CODE)
    URL = IAM_HOST + API
    headers = {
        "X-Bk-App-Code": APP_CODE,
        "X-Bk-App-Secret": SECRET_KEY,
        "Content-Type": "application/json"
    }
    res = requests.post(URL, headers=headers, json=actions)

