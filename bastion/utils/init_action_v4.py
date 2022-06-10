import os
import requests


def add_action_to_system():
    IAM_HOST = os.getenv("BK_IAM_V3_INNER_HOST", "http://bkiam.service.consul:5001")
    APP_CODE = os.getenv("APP_ID")
    SECRET_KEY = os.getenv("APP_TOKEN")
    actions = [
        # 主机资源
        {"id": "get-host-resources", "name": "查看主机资源详情", "name_en": "get host resources", "description": "查看主机资源详情", "description_en": "get host resources", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-host-resources", "name": "编辑主机资源", "name_en": "modify host resources", "description": "编辑主机资源", "description_en": "modify host resources", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "login-host-resources", "name": "登陆主机资源", "name_en": "login host resources", "description": "登陆主机资源", "description_en": "login host resources", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-host-resources", "name": "删除主机资源", "name_en": "delete host resources", "description": "删除主机资源", "description_en": "delete host resources", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "create-host-resources", "name": "创建主机资源", "name_en": "create host resources", "description": "创建主机资源", "description_en": "create host resources", "type": "view", "related_resource_types": [], "version": 1},
        # 密码凭证
        {"id": "get-password-voucher", "name": "查看密码凭证详情", "name_en": "get password voucher", "description": "查看密码凭证详情", "description_en": "get password voucher", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-password-voucher", "name": "编辑密码凭证", "name_en": "modify password voucher", "description": "编辑密码凭证", "description_en": "modify password voucher", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-password-voucher", "name": "删除密码凭证", "name_en": "delete password voucher", "description": "删除密码凭证", "description_en": "delete password voucher", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "create-password-voucher", "name": "创建密码凭证", "name_en": "create password voucher", "description": "创建密码凭证", "description_en": "create password voucher", "type": "view", "related_resource_types": [], "version": 1},
        # SSH凭证
        {"id": "get-ssh-voucher", "name": "查看SSH凭证详情", "name_en": "get ssh voucher", "description": "查看SSH凭证详情", "description_en": "get ssh voucher", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-ssh-voucher", "name": "编辑SSH凭证", "name_en": "modify ssh voucher", "description": "编辑SSH凭证", "description_en": "modify ssh voucher", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-ssh-voucher", "name": "删除SSH凭证", "name_en": "delete ssh voucher", "description": "删除SSH凭证", "description_en": "delete ssh voucher", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "create-ssh-voucher", "name": "创建SSH凭证", "name_en": "create ssh voucher", "description": "创建SSH凭证", "description_en": "create ssh voucher", "type": "view", "related_resource_types": [], "version": 1},
        # 凭证分组
        {"id": "get-voucher-group", "name": "查看凭证分组详情", "name_en": "get voucher group", "description": "查看凭证分组详情", "description_en": "get voucher group", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-voucher-group", "name": "编辑凭证分组", "name_en": "modify voucher group", "description": "编辑凭证分组", "description_en": "modify voucher group", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-voucher-group", "name": "删除凭证分组", "name_en": "delete voucher group", "description": "删除凭证分组", "description_en": "delete voucher group", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "create-voucher-group", "name": "创建凭证分组", "name_en": "create voucher group", "description": "创建凭证分组", "description_en": "create voucher group", "type": "view", "related_resource_types": [], "version": 1},
        # 访问策略
        {"id": "get-access-credential", "name": "查看访问策略详情", "name_en": "get access credential", "description": "查看访问策略详情", "description_en": "get access credential", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-access-credential", "name": "编辑访问策略", "name_en": "modify access credential", "description": "编辑访问策略", "description_en": "modify access credential", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-access-credential", "name": "删除访问策略", "name_en": "delete access credential", "description": "删除访问策略", "description_en": "delete access credential", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "create-access-credential", "name": "创建访问策略", "name_en": "create access credential", "description": "创建访问策略", "description_en": "create access credential", "type": "view", "related_resource_types": [], "version": 1},
        # 命令策略
        {"id": "get-command-credential", "name": "查看命令策略详情", "name_en": "get command credential", "description": "查看命令策略详情", "description_en": "get command credential", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-command-credential", "name": "编辑命令策略", "name_en": "modify command credential", "description": "编辑命令策略", "description_en": "modify command credential", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-command-credential", "name": "删除命令策略", "name_en": "delete command credential", "description": "删除命令策略", "description_en": "delete command credential", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "create-command-credential", "name": "创建命令策略", "name_en": "create command credential", "description": "创建命令策略", "description_en": "create command credential", "type": "view", "related_resource_types": [], "version": 1},
        # 命令列表
        {"id": "get-command-list", "name": "查看命令列表", "name_en": "get command list", "description": "查看命令列表", "description_en": "get command list", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-command-list", "name": "编辑命令列表", "name_en": "modify command list", "description": "编辑命令列表", "description_en": "modify command list", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-command-list", "name": "删除命令列表", "name_en": "delete command list", "description": "删除命令列表", "description_en": "delete command list", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "create-command-list", "name": "创建命令列表", "name_en": "create command list", "description": "创建命令列表", "description_en": "create command list", "type": "view", "related_resource_types": [], "version": 1},
        # 命令组
        {"id": "get-command-group", "name": "查看命令组", "name_en": "get command group", "description": "查看命令组", "description_en": "get command group", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-command-group", "name": "编辑命令组", "name_en": "modify command group", "description": "编辑命令组", "description_en": "modify command group", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-command-group", "name": "删除命令组", "name_en": "delete command group", "description": "删除命令组", "description_en": "delete command group", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "create-command-group", "name": "创建命令组", "name_en": "create command group", "description": "创建命令组", "description_en": "create command group", "type": "view", "related_resource_types": [], "version": 1},
        # 在线会话
        {"id": "logout-session", "name": "强制下线", "name_en": "logout session", "description": "强制下线", "description_en": "logout session", "type": "view", "related_resource_types": [], "version": 1},
        # 历史会话
        {"id": "play-history", "name": "播放历史", "name_en": "play history", "description": "播放历史", "description_en": "play history", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "get-history", "name": "查看历史详情", "name_en": "get history", "description": "查看历史详情", "description_en": "play history", "type": "view", "related_resource_types": [], "version": 1},
        # 授权主机
        {"id": "login-authorization-host", "name": "登陆授权主机", "name_en": "login authorization host", "description": "查看历史详情", "description_en": "login authorization host", "type": "view", "related_resource_types": [], "version": 1},
        # 用户管理
        {"id": "import-user", "name": "导入用户", "name_en": "import user", "description": "导入用户", "description_en": "import user", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-user", "name": "移除用户", "name_en": "delete user", "description": "移除用户", "description_en": "delete user", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "get-user-group", "name": "查看用户组", "name_en": "get user group", "description": "查看用户组", "description_en": "get user group", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "create-user-group", "name": "新建用户组", "name_en": "create user group", "description": "新建用户组", "description_en": "create user group", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-user-group", "name": "编辑用户组", "name_en": "modify user group", "description": "编辑用户组", "description_en": "modify user group", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-user-group", "name": "删除用户组", "name_en": "delete user group", "description": "删除用户组", "description_en": "delete user group", "type": "view", "related_resource_types": [], "version": 1},
        # 网络代理
        {"id": "create-network-proxy", "name": "创建网络代理", "name_en": "create network proxy", "description": "创建网络代理", "description_en": "create network proxy", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "modify-network-proxy", "name": "编辑网络代理", "name_en": "modify network proxy", "description": "编辑网络代理", "description_en": "modify network proxy", "type": "view", "related_resource_types": [], "version": 1},
        {"id": "delete-network-proxy", "name": "删除网络代理", "name_en": "delete network proxy", "description": "删除网络代理", "description_en": "delete network proxy", "type": "view", "related_resource_types": [], "version": 1},
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