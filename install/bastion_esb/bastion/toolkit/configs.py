# -*- coding: utf-8 -*-
from esb.utils import SmartHost


# 系统名的小写形式，与系统包名保持一致
SYSTEM_NAME = 'BASTION'

host = SmartHost(
    # 需要填入系统正式环境的域名地址
    host_prod='paas.bksingle.com',
)
