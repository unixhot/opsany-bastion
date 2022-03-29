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
        },{
            "id": "visit-password-voucher",
            "name": "访问密码凭证",
            "name_en": "visit password voucher",
            "description": "访问密码凭证",
            "description_en": "visit password voucher",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "visit-ssh-voucher",
            "name": "访问SSH凭证",
            "name_en": "visit ssh voucher",
            "description": "访问SSH凭证",
            "description_en": "visit ssh voucher",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "visit-voucher-group",
            "name": "访问凭证分组",
            "name_en": "visit voucher group",
            "description": "访问凭证分组",
            "description_en": "visit voucher group",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "use-access-credential",
            "name": "使用访问策略",
            "name_en": "use access credential",
            "description": "使用访问策略",
            "description_en": "use access credential",
            "type": "use",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "use-command-credential",
            "name": "使用命令策略",
            "name_en": "use command credential",
            "description": "使用命令策略",
            "description_en": "use command credential",
            "type": "use",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "visit-online-session",
            "name": "访问在线会话",
            "name_en": "visit online session",
            "description": "访问在线会话",
            "description_en": "visit online session",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "visit-history-session",
            "name": "访问历史会话",
            "name_en": "visit history session",
            "description": "访问历史会话",
            "description_en": "visit history session",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "visit-audit-history",
            "name": "访问审计历史",
            "name_en": "visit audit history",
            "description": "访问审计历史",
            "description_en": "visit audit history",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "visit-operation-log",
            "name": "访问操作日志",
            "name_en": "visit operation log",
            "description": "访问操作日志",
            "description_en": "visit operation log",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "visit-authorization-host",
            "name": "访问授权主机",
            "name_en": "visit authorization host",
            "description": "访问授权主机",
            "description_en": "visit authorization host",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "visit-user-admin",
            "name": "访问用户管理",
            "name_en": "visit user admin",
            "description": "访问用户管理",
            "description_en": "visit user admin",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }, {
            "id": "visit-network-proxy",
            "name": "访问网络代理",
            "name_en": "visit network proxy",
            "description": "访问网络代理",
            "description_en": "visit network proxy",
            "type": "view",
            "related_resource_types": [],
            "version": 1
        }
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
    print(res.json())


if __name__ == '__main__':
    add_action_to_system()
