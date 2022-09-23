# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = ['celery_app', 'RUN_VER', 'APP_CODE', 'SECRET_KEY', 'BK_URL', 'BASE_DIR']

import os

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from blueapps.core.celery import celery_app

# app 基本信息
def get_env_or_raise(key):
    """Get an environment variable, if it does not exist, raise an exception"""
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(
            (
                'Environment variable "{}" not found, you must set this variable to run this application.'
            ).format(key)
        )
    return value

# SaaS运行版本，如非必要请勿修改
RUN_VER = 'open'
# SaaS应用ID
APP_CODE = os.getenv("BKPAAS_APP_ID", "opsany-bastion")
# SaaS安全密钥，注意请勿泄露该密钥
SECRET_KEY = os.getenv("BKPAAS_APP_SECRET")
# PAAS平台URL
# 注意： 不能用这个变量来作为 ESB API 的 URL 前缀
BK_URL = os.getenv("BKPAAS_URL")
# ESB API 访问 URL
BK_COMPONENT_API_URL = os.getenv("BK_COMPONENT_API_URL")

# UploadPath
UPLOAD_PATH = os.getenv("BK_APP_UPLOAD_PATH", "/opt/opsany/")
# IAM URL
BK_IAM_HOST = os.getenv("BK_IAM_V3_INNER_HOST", "http://bkiam.service.consul:5001")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(
    __file__)))
