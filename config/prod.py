# -*- coding: utf-8 -*-
from config import RUN_VER, UPLOAD_PATH

if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 正式环境
RUN_MODE = 'PRODUCT'

# 只对正式环境日志级别进行配置，可以在这里修改
LOG_LEVEL = 'ERROR'

# V2
# import logging
# logging.getLogger('root').setLevel('INFO')
# V3
# import logging
# logging.getLogger('app').setLevel('INFO')

GUACD_HOST = '127.0.0.1'
GUACD_PORT = '4822'
# 对应guacd的路径如下
GUACD_PATH = "/srv/guacamole"

MEDIA_URL = ''
TERMINAL_PATH = os.path.join(UPLOAD_PATH, "uploads/terminal")
ORI_GUACD_PATH = os.path.join(UPLOAD_PATH, "uploads/guacamole")
TERMINAL_TIMEOUT = int(os.getenv("BKAPP_TERMINAL_TIMEOUT", 1800))

DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bastion',  # 数据库名
            'USER': 'bastion',  # 数据库用户
            'PASSWORD': os.getenv("BKAPP_MYSQL_PASSWORD", "bastion"),  # 数据库密码
            'HOST': os.getenv("BKAPP_MYSQL_HOST", "172.16.16.3"),  # 数据库主机
            'PORT': int(os.getenv("BKAPP_MYSQL_PORT", "3306")),  # 数据库端口
        },
    }
)

REDIS_HOST = os.getenv("BKAPP_REDIS_HOST", "172.16.16.3")
REDIS_PORT = os.getenv("BKAPP_REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("BKAPP_REDIS_PASSWORD", "DRwsgTKXUsEY")

CACHES.update(
    {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://{REDIS_HOST}:{REDIS_PORT}/1".format(REDIS_HOST=REDIS_HOST, REDIS_PORT=REDIS_PORT),
            'TIMEOUT': 86400,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_KWARGS": {"max_connections": 1000},
                "PASSWORD": REDIS_PASSWORD,
            }
        },
        "cache": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://{REDIS_HOST}:{REDIS_PORT}/9".format(REDIS_HOST=REDIS_HOST, REDIS_PORT=REDIS_PORT),
            'TIMEOUT': 1800,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_KWARGS": {"max_connections": 1000},
                "PASSWORD": REDIS_PASSWORD,
            }
        }
    }
)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': ['redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/8'.format(REDIS_PASSWORD=REDIS_PASSWORD, REDIS_HOST=REDIS_HOST, REDIS_PORT=REDIS_PORT)],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    }
}
