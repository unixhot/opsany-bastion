# -*- coding: utf-8 -*-
from config import RUN_VER

if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 本地开发环境
RUN_MODE = 'DEVELOP'

# APP本地静态资源目录
STATIC_URL = '/static/'

# pycryptodomex             3.9.8
# APP静态资源目录url
# REMOTE_STATIC_URL = '%sremote/' % STATIC_URL

# Celery 消息队列设置 RabbitMQ
# BROKER_URL = 'amqp://opsany:123456.coM@123.56.111.149:5672//'
# Celery 消息队列设置 Redis
# BROKER_URL = 'redis://127.0.0.1:6379/8'


DEBUG = True

TERMINAL_PATH = os.getenv("TERMINAL_PATH", "D:/womaiyun/upload/terminal")
GUACD_HOST = '127.0.0.1'
GUACD_PORT = '4822'
# paas服务器本地路径，
ORI_GUACD_PATH = '/opt/dev-paas/uploads/guacamole/'
GUACD_PATH = '/srv/guacamole'
# 堡垒机超时时间，单位s
TERMINAL_TIMEOUT = 1800
MEDIA_URL = ''
UPLOAD_PATH = '/opt/opsany/'
# 本地开发数据库设置
# USE FOLLOWING SQL TO CREATE THE DATABASE NAMED APP_CODE
# SQL: CREATE DATABASE `framework_py` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; # noqa: E501
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "bk-bastion",
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        'TIMEOUT': 86400,  # 1天
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 1000},
            # "PASSWORD": REDIS_PASSWORD
        }
        },
    "cache": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/9",
        'TIMEOUT': 1800,  # 30分钟
        "OPTIONS": {
            "CLIENT_CALSS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 1000},
            # "PASSWORD": "123456.coM",
        }
    }
}

CHANNEL_LAYERS = {
    'default': {
        # 'BACKEND': 'asgi_redis.RedisChannelLayer',
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': ['redis://:DRwsgTKXUsEY@localhost:6379/8'],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
        # 'ROUTING': 'shell.routing.channel_routing',
    }
}

# 自定义中间件
MIDDLEWARE += (
    'bastion.utils.middleware.LocalLoginDebugMiddleware',
)


# 多人开发时，无法共享的本地配置可以放到新建的 local_settings.py 文件中
# 并且把 local_settings.py 加入版本管理忽略文件中
try:
    from .local_settings import *  # noqa
except ImportError:
    pass
