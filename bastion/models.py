import datetime

from django.db import models
import logging

from bastion.utils.base_model import BaseModel

app_logging = logging.getLogger("app")


# 用户体系
class UserInfo(BaseModel):
    phone = models.CharField(max_length=30, null=True, verbose_name="手机号")
    username = models.CharField(max_length=50, verbose_name="用户名")
    email = models.CharField(max_length=255, null=True, verbose_name="邮箱")
    ch_name = models.CharField(max_length=50, null=True, verbose_name="中文名")
    role = models.IntegerField(verbose_name="用户角色")

    class Meta:
        db_table = "user_info"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def to_base_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "ch_name": self.ch_name,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "username": self.username,
            "email": self.email,
            "ch_name": self.ch_name,
            "role": self.role,
        }

    def get_user_strategy_access_queryset(self):
        # strategy_access_user_group_queryset = StrategyAccessUserGroupRelationshipModel.fetch_all(status=True)
        strategy_access_user_group_queryset = list(self.user_strategy_access.get_queryset())
        for group_user in self.user_group.get_queryset():
            strategy_access_user_group_queryset.extend(group_user.user_group.user_group_strategy_access.get_queryset())
        strategy_access_queryset = list(
            set([strategy_user.strategy_access for strategy_user in strategy_access_user_group_queryset]))
        # 校验有效时间和开启状态
        login_time_open_strategy_access_query = list()
        for strategy_access_query in strategy_access_queryset:
            check_time = self.check_strategy_valid(strategy_access_query)
            if check_time and strategy_access_query not in login_time_open_strategy_access_query:
                login_time_open_strategy_access_query.append(strategy_access_query)
        return login_time_open_strategy_access_query

    def get_user_strategy_access_queryset_v3(self):
        strategy_access_user_group_queryset = list(self.user_strategy_access.get_queryset())
        for group_user in self.user_group.get_queryset():
            strategy_access_user_group_queryset.extend(group_user.user_group.user_group_strategy_access.get_queryset())
        strategy_access_queryset = list(
            set([strategy_user.strategy_access for strategy_user in strategy_access_user_group_queryset]))
        # 状态开启，有效期内，登录时段外（登录变灰）
        login_time_open_strategy_access_query = list()
        # 状态开启，有效期内，登录时段内（正常）
        time_frame_open_strategy_access_query = list()
        for strategy_access_query in strategy_access_queryset:
            check_time = self.check_strategy_valid_v3(strategy_access_query)
            print("check_time", check_time)
            if check_time and strategy_access_query not in login_time_open_strategy_access_query:
                login_time_open_strategy_access_query.append(strategy_access_query)
        return login_time_open_strategy_access_query

    def check_strategy_valid_v3(self, strategy_query):
        # 0 关闭，不在有效期 1. 在有效期内，不在登录时段内 2 在登录时段内
        now_datetime = datetime.datetime.now()
        week_day = datetime.datetime.now().isoweekday()
        hour = datetime.datetime.now().hour
        if strategy_query.status:
            check_time = 1
        else:
            return 0
        start_time = strategy_query.start_time
        end_time = strategy_query.end_time
        if start_time and not end_time:
            if now_datetime > start_time:
                check_time = 1
            else:
                return 0
        if end_time and not start_time:
            if now_datetime < end_time:
                check_time = 1
            else:
                return 0
        if end_time and start_time:
            if start_time < now_datetime < end_time:
                check_time = 1
            else:
                return 0
        if not start_time and not end_time:
            check_time = 1
        if strategy_query.login_time_limit:
            try:
                in_login_time_limit = list()
                for _login_time_limit in eval(strategy_query.login_time_limit):
                    if _login_time_limit.get("week") == week_day:
                        if hour in _login_time_limit.get("time"):
                            in_login_time_limit.append((week_day, hour))
                            break
                if in_login_time_limit:
                    check_time = 2
            except Exception as e:
                return 0
        return check_time

    def check_strategy_valid(self, strategy_query):
        now_datetime = datetime.datetime.now()
        week_day = datetime.datetime.now().isoweekday()
        hour = datetime.datetime.now().hour
        check_time = False
        if strategy_query.status:
            check_time = True
        else:
            return False
        start_time = strategy_query.start_time
        end_time = strategy_query.end_time
        if start_time and not end_time:
            if now_datetime > start_time:
                check_time = True
            else:
                return False
        if end_time and not start_time:
            if now_datetime < end_time:
                check_time = True
            else:
                return False
        if end_time and start_time:
            if start_time < now_datetime < end_time:
                check_time = True
            else:
                return False
        if not start_time and not end_time:
            check_time = True
        if strategy_query.login_time_limit:
            try:
                in_login_time_limit = list()
                for _login_time_limit in eval(strategy_query.login_time_limit):
                    if _login_time_limit.get("week") == week_day:
                        if hour in _login_time_limit.get("time"):
                            in_login_time_limit.append((week_day, hour))
                            break
                if in_login_time_limit:
                    check_time = True
                else:
                    return False
            except Exception as e:
                return False
        return check_time

    def get_host_credential_queryset(self):
        strategy_access_queryset = self.get_user_strategy_access_queryset()
        strategy_access_credential_host_queryset = StrategyAccessCredentialHostModel.fetch_all(
            strategy_access__in=strategy_access_queryset)
        host_credential_queryset = [strategy_access_credential_host_query.credential_host for
                                    strategy_access_credential_host_query in strategy_access_credential_host_queryset if
                                    strategy_access_credential_host_query.credential_host]
        credential_group_queryset = [strategy_access_credential_host_query.credential_group for
                                     strategy_access_credential_host_query in strategy_access_credential_host_queryset
                                     if
                                     strategy_access_credential_host_query.credential_group]
        host_credential_queryset.extend(
            HostCredentialRelationshipModel.fetch_all(credential_group__in=credential_group_queryset))
        return list(set(host_credential_queryset))

    def get_host_credential_queryset_v3(self):
        strategy_access_queryset = self.get_user_strategy_access_queryset_v3()
        strategy_access_credential_host_queryset = StrategyAccessCredentialHostModel.fetch_all(
            strategy_access__in=strategy_access_queryset)
        host_credential_queryset = [strategy_access_credential_host_query.credential_host for
                                    strategy_access_credential_host_query in strategy_access_credential_host_queryset if
                                    strategy_access_credential_host_query.credential_host]
        credential_group_queryset = [strategy_access_credential_host_query.credential_group for
                                     strategy_access_credential_host_query in strategy_access_credential_host_queryset
                                     if
                                     strategy_access_credential_host_query.credential_group]
        host_credential_queryset.extend(
            HostCredentialRelationshipModel.fetch_all(credential_group__in=credential_group_queryset))
        return list(set(host_credential_queryset))

    def get_user_credential_queryset(self):
        # 通过用户查询授权的凭据
        # 1. 获取访问策略
        strategy_access_queryset = self.get_user_strategy_access_queryset()
        credential_strategy_rel_queryset = []
        credential_group_rel_queryset = []
        # 2. 获取策略相关凭据
        for strategy_access in strategy_access_queryset:
            credential_strategy_rel_queryset.extend(
                strategy_access.strategy_access_credential_or_credential_group.get_queryset())
        credential_queryset = [credential_strategy.credential for credential_strategy in
                               credential_strategy_rel_queryset if credential_strategy.credential]
        # 3. 获取策略相关凭据组
        credential_group_queryset = [credential_strategy.credential_group for credential_strategy in
                                     credential_strategy_rel_queryset if credential_strategy.credential_group]
        for credential_group in credential_group_queryset:
            credential_group_rel_queryset.extend(credential_group.credential_group_queryset.get_queryset())
        # 4. 增加凭据组内凭据
        for credential_group_query in credential_group_rel_queryset:
            credential_queryset.append(credential_group_query.credential)
        return list(set(credential_queryset))

    def get_auth_host_credential_queryset(self):
        host_credential_queryset = self.get_host_credential_queryset()
        resource_credential = [host_credential_query for host_credential_query in host_credential_queryset]
        return resource_credential

    def get_user_host_queryset(self):
        credential_queryset = self.get_user_credential_queryset()
        host_credential_queryset = []
        host_queryset = []
        for credential in credential_queryset:
            host_credential_queryset.extend(credential.credential_host.get_queryset())
        for host_credential in host_credential_queryset:
            host_queryset.append(host_credential.host)
        return list(set(host_queryset))

    def get_user_host_queryset_v2(self):
        host_credential_queryset = self.get_host_credential_queryset()
        host_queryset = [host_credential_query.host for host_credential_query in host_credential_queryset]
        return list(set(host_queryset))

    def get_user_host_queryset_v3(self):
        # 当有关联策略且状态为开启，时显示列表，否则不显示
        # 当登录时段被限制时登录按钮变灰，否则正常
        host_credential_queryset = self.get_host_credential_queryset_v3()
        host_queryset = [host_credential_query.host for host_credential_query in host_credential_queryset]
        return list(set(host_queryset))

    def get_user_host_in_group(self, group, search_data=None):
        host_credential_queryset = self.get_host_credential_queryset()
        host_queryset = []
        for host_credential_query in host_credential_queryset:
            if host_credential_query.host.group == group:
                if search_data:
                    if search_data in host_credential_query.host.host_name or search_data in host_credential_query.host.host_address:
                        host_queryset.append(host_credential_query.host)
                else:
                    host_queryset.append(host_credential_query.host)
        return list(set(host_queryset))

    def get_strategy_command_queryset(self):
        user_strategy_command_queryset = list(self.user_strategy_command.get_queryset())
        for group_user in self.user_group.get_queryset():
            user_strategy_command_queryset.extend(group_user.user_group.user_group_strategy_command.get_queryset())
        all_strategy_command_queryset = [strategy_command_user_group.strategy_command for strategy_command_user_group in
                                         user_strategy_command_queryset]
        login_time_open_strategy_command_query = list()
        for strategy_command_query in all_strategy_command_queryset:
            check_time = self.check_strategy_command_valid(strategy_command_query)
            if check_time and strategy_command_query not in login_time_open_strategy_command_query:
                login_time_open_strategy_command_query.append(strategy_command_query)
        return login_time_open_strategy_command_query

    def check_strategy_command_valid(self, strategy_query):
        now_datetime = datetime.datetime.now()
        week_day = datetime.datetime.now().isoweekday()
        hour = datetime.datetime.now().hour
        check_time = False
        if strategy_query.status:
            check_time = True
        else:
            return False
        start_time = strategy_query.start_time
        end_time = strategy_query.end_time
        if start_time and not end_time:
            if now_datetime > start_time:
                check_time = True
            else:
                return False
        if end_time and not start_time:
            if now_datetime < end_time:
                check_time = True
            else:
                return False
        if end_time and start_time:
            if start_time < now_datetime < end_time:
                check_time = True
            else:
                return False
        if not start_time and not end_time:
            check_time = True
        if strategy_query.login_time_limit:
            try:
                in_login_time_limit = list()
                for _login_time_limit in eval(strategy_query.login_time_limit):
                    if _login_time_limit.get("week") == week_day:
                        if hour in _login_time_limit.get("time"):
                            in_login_time_limit.append((week_day, hour))
                            break
                if in_login_time_limit:
                    check_time = False
                else:
                    return True
            except Exception as e:
                return False
        return check_time


# 用户组
class UserGroupModel(BaseModel):
    name = models.CharField(max_length=50, verbose_name="用户组名称")
    description = models.CharField(max_length=500, unique=False, null=True, blank=True, verbose_name="描述")

    class Meta:
        db_table = "user_group"
        verbose_name = "用户组"
        verbose_name_plural = verbose_name

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
        return dic

    def to_list_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
        all_rel = self.group_user.get_queryset()
        user_list = []
        for rel in all_rel:
            if rel and rel.user:
                user_list.append({
                    "id": rel.user.id,
                    "ch_name": rel.user.ch_name,
                    "username": rel.user.username,
                    "email": rel.user.email,
                    "role": rel.user.role,
                    "phone": rel.user.phone
                })
        dic["user_list"] = user_list
        return dic


# 用户、组关联表
class UserGroupRelationshipModel(BaseModel):
    user_group = models.ForeignKey(UserGroupModel, related_name="group_user", on_delete=models.CASCADE,
                                   verbose_name="组")
    user = models.ForeignKey(UserInfo, models.CASCADE, related_name="user_group", db_index=True, verbose_name="用户")

    class Meta:
        db_table = "group_user_relationship"
        verbose_name = "用户、组关联表"
        verbose_name_plural = verbose_name

    def to_dict(self):
        dic = {
            "id": self.id,
            "group": self.user_group.to_dict(),
            "user": self.user.to_dict(),
        }
        return dic


# 访问策略
class StrategyAccessModel(BaseModel):
    DEFAULT_LOGIN_TIME = [
        {"week": 1, "time": []},
        {"week": 2, "time": []},
        {"week": 3, "time": []},
        {"week": 4, "time": []},
        {"week": 5, "time": []},
        {"week": 6, "time": []},
        {"week": 7, "time": []}
    ]
    name = models.CharField(max_length=50, verbose_name="策略名称", unique=True)
    start_time = models.DateTimeField(verbose_name="生效时间", null=True)
    end_time = models.DateTimeField(verbose_name="失效时间", null=True)
    file_upload = models.BooleanField(default=False, verbose_name="文件上传")
    file_download = models.BooleanField(default=False, verbose_name="文件下载")
    file_manager = models.BooleanField(default=False, verbose_name="文件管理")
    copy_tool = models.BooleanField(default=False, verbose_name="剪切板")
    login_time_limit = models.TextField(blank=True, verbose_name="登录时段限制", null=True)
    # 1 无  2 黑名单  3 白名单
    ip_limit = models.IntegerField(default=1)
    limit_list = models.TextField()
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "strategy_access"
        verbose_name = "访问策略"
        verbose_name_plural = verbose_name

    def get_list_field(self, field):
        try:
            if field:
                return eval(field)
            else:
                return []
        except Exception as e:
            app_logging.error("[ERROR] StrategyAccessModel eval error: {}, param: {}".format(str(e), str(field)))
            return []

    def to_dict(self):
        dt = {
            "id": self.id,
            "name": self.name,
            "create_time": str(self.create_time).rsplit(".", 1)[0] if self.create_time else "",
            "start_time": str(self.start_time).rsplit(".", 1)[0] if self.start_time else "",
            "end_time": str(self.end_time).rsplit(".", 1)[0] if self.end_time else "",
            "file_upload": self.file_upload,
            "file_download": self.file_download,
            "file_manager": self.file_manager,
            "status": self.status,
            "ip_limit": self.ip_limit,
            "limit_list": self.get_list_field(self.limit_list),
            "login_time_limit": self.get_list_field(self.login_time_limit) if self.get_list_field(
                self.login_time_limit) else self.DEFAULT_LOGIN_TIME,
            "copy_tool": self.copy_tool
        }
        return dt

    def to_all_dict(self):
        dt = {
            "strategy": self.to_dict(),
            "user": {
                "user": [],
                "user_group": []
            },
            "credential_host": {
                "ssh_credential_host_id": [],
                "password_credential_host_id": [],
                "credential_group": []
            }
        }
        if self.strategy_access_user_or_user_group.get_queryset():
            user_list = []
            user_group_list = []
            for _query in self.strategy_access_user_or_user_group.get_queryset():
                if _query.user:
                    user_list.append(_query.user.id)
                if _query.user_group:
                    user_group_list.append(_query.user_group.id)
            dt["user"].update({"user": user_list})
            dt["user"].update({"user_group": user_group_list})
        if self.new_strategy_access_credential_or_credential_group.get_queryset():
            ssh_credential_host = []
            password_credential_host = []
            credential_group = []
            for _query in self.new_strategy_access_credential_or_credential_group.get_queryset():
                if _query.credential_host:
                    if _query.credential_host.credential.credential_type == CredentialModel.CREDENTIAL_SSH_KEY:
                        ssh_credential_host.append(_query.credential_host.to_dict())
                    if _query.credential_host.credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                        password_credential_host.append(_query.credential_host.to_dict())
                if _query.credential_group:
                    credential_group.append(_query.credential_group.to_base_dict())
            dt["credential_host"].update({"ssh_credential_host_id": ssh_credential_host})
            dt["credential_host"].update({"password_credential_host_id": password_credential_host})
            dt["credential_host"].update({"credential_group": credential_group})
        return dt

    def to_list_dict(self):
        dt = {
            "id": self.id,
            "name": self.name,
            "create_time": str(self.create_time).rsplit(".", 1)[0] if self.create_time else "",
            "start_time": str(self.start_time).rsplit(".", 1)[0] if self.start_time else "",
            "end_time": str(self.end_time).rsplit(".", 1)[0] if self.end_time else "",
            "file_upload": self.file_upload,
            "file_download": self.file_download,
            "file_manager": self.file_manager,
            "status": self.status,
            "ip_limit": self.ip_limit,
            "limit_list": self.get_list_field(self.limit_list),
            "login_time_limit": self.get_list_field(self.login_time_limit) if self.get_list_field(
                self.login_time_limit) else self.DEFAULT_LOGIN_TIME,
            "copy_tool": self.copy_tool,
            "user": {
                "user": [],
                "user_group": []
            },
            "credential_host": {
                "ssh_credential_host_id": [],
                "password_credential_host_id": [],
                "credential_group": []
            }
        }
        if self.strategy_access_user_or_user_group.get_queryset():
            user_list = []
            user_group_list = []
            for _query in self.strategy_access_user_or_user_group.get_queryset():
                if _query.user:
                    user_list.append({"user_id": _query.user.id, "user_name": _query.user.username})
                if _query.user_group:
                    user_group_list.append(
                        {"user_group_id": _query.user_group.id, "user_group_name": _query.user_group.name})
            dt["user"].update({"user": user_list})
            dt["user"].update({"user_group": user_group_list})
        if self.new_strategy_access_credential_or_credential_group.get_queryset():
            ssh_credential_host = []
            password_credential_host = []
            credential_group = []
            for _query in self.new_strategy_access_credential_or_credential_group.get_queryset():
                if _query.credential_host:
                    if _query.credential_host.credential.credential_type == CredentialModel.CREDENTIAL_SSH_KEY:
                        ssh_credential_host.append({"credential_host_id": _query.credential_host.id})
                    if _query.credential_host.credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                        password_credential_host.append({"credential_host_id": _query.credential_host.id})
                if _query.credential_group:
                    credential_group.append({"credential_group_id": _query.credential_group.id})
            dt["credential_host"].update({"ssh_credential_host_id": ssh_credential_host})
            dt["credential_host"].update({"password_credential_host_id": password_credential_host})
            dt["credential_host"].update({"credential_group": credential_group})
        return dt


# 访问策略关联用户，用户组
class StrategyAccessUserGroupRelationshipModel(BaseModel):
    strategy_access = models.ForeignKey(StrategyAccessModel, on_delete=models.CASCADE, verbose_name="关联策略",
                                        related_name="strategy_access_user_or_user_group")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank=True, verbose_name="关联用户",
                             related_name="user_strategy_access")
    user_group = models.ForeignKey(UserGroupModel, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="关联用户组", related_name="user_group_strategy_access")

    class Meta:
        db_table = "strategy_access_user_group_relationship"
        verbose_name = "访问策略关联用户，用户组"
        verbose_name_plural = verbose_name

    def to_dict(self):
        dic = {
            "id": self.id,
            "strategy": self.strategy_access.to_dict(),
            "user": self.user.to_dict(),
            "user_group": self.user_group.to_dict()
        }
        return dic


# 命令
class CommandModel(BaseModel):
    command = models.CharField(max_length=255, verbose_name="命令名称")
    # 1 阻断  2 提醒
    block_type = models.IntegerField(default=1, verbose_name="阻断类型")
    block_info = models.CharField(max_length=255, verbose_name="阻断提示信息")
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    class Meta:
        db_table = "command"
        verbose_name = "命令"
        verbose_name_plural = verbose_name

    def to_base_dict(self):
        dic = {
            "id": self.id,
            "command": self.command,
            "block_type": self.block_type,
            "block_info": self.block_info
        }
        return dic

    def to_dict(self):
        dic = {
            "id": self.id,
            "command": self.command,
            "block_type": self.block_type,
            "block_info": self.block_info
        }
        if self.user:
            dic["user"] = self.user.to_base_dict()
        if self.get_command_group():
            dic["command_group"] = self.get_command_group()
        return dic

    def get_command_group(self):
        command_group_queryset = self.command_queryset.get_queryset()
        command_group = [command_group.command_group.to_base_dict() for command_group in command_group_queryset]
        return command_group


# 命令分组
class CommandGroupModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name="命令分组名称")
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name="描述")
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    class Meta:
        db_table = "command_group"
        verbose_name = "命令分组"
        verbose_name_plural = verbose_name

    def to_base_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
        }
        return dic

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "create_time": str(self.create_time).rsplit(".")[0]
        }
        if self.get_command_list():
            dic["command"] = self.get_command_list()
        return dic

    def to_all_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "create_time": str(self.create_time).rsplit(".")[0]
        }
        if self.get_command_list():
            dic["command"] = self.get_command_list()
        return dic

    def get_command_list(self):
        return [command_group.command.to_base_dict() for command_group in self.command_group_queryset.get_queryset()]


# 命令分组关联
class CommandGroupRelationshipModel(BaseModel):
    command = models.ForeignKey(CommandModel, on_delete=models.CASCADE, related_name="command_queryset",
                                verbose_name="命令")
    command_group = models.ForeignKey(CommandGroupModel, on_delete=models.CASCADE,
                                      related_name="command_group_queryset", null=True, verbose_name="命令分组")

    class Meta:
        db_table = "command_group_relationship"
        verbose_name = "命令分组关联"
        verbose_name_plural = verbose_name
        unique_together = (("command", "command_group"),)

    def to_dict(self):
        dic = {
            "id": self.id,
            "command": self.command.to_dict(),
            "command_group": self.command_group.to_dict()
        }
        return dic


# 命令策略
class StrategyCommandModel(BaseModel):
    DEFAULT_LOGIN_TIME = [
        {"week": 1, "time": []},
        {"week": 2, "time": []},
        {"week": 3, "time": []},
        {"week": 4, "time": []},
        {"week": 5, "time": []},
        {"week": 6, "time": []},
        {"week": 7, "time": []}
    ]
    name = models.CharField(max_length=50, unique=True, verbose_name="命令策略名称")
    start_time = models.DateTimeField(verbose_name="生效时间", null=True)
    end_time = models.DateTimeField(verbose_name="失效时间", null=True)
    login_time_limit = models.TextField(blank=True, verbose_name="登录时段限制")
    status = models.BooleanField(default=True)
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    class Meta:
        db_table = "strategy_command"
        verbose_name = "命令策略"
        verbose_name_plural = verbose_name

    def get_list_field(self, field):
        try:
            if field:
                return eval(field)
            else:
                return []
        except Exception as e:
            app_logging.error("[ERROR] StrategyCommandModel eval error: {}, param: {}".format(str(e), str(field)))
            return []

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "start_time": str(self.start_time).rsplit(".", 1)[0] if self.start_time else "",
            "end_time": str(self.end_time).rsplit(".", 1)[0] if self.end_time else "",
            "create_time": str(self.create_time).rsplit(".", 1)[0] if self.create_time else "",
            "login_time_limit": self.get_list_field(self.login_time_limit) if self.get_list_field(
                self.login_time_limit) else self.DEFAULT_LOGIN_TIME,
        }
        return dic

    def to_all_dict(self):
        dt = {
            "strategy": self.to_dict(),
            "user": {
                "user": [],
                "user_group": []
            },
            "command": {
                "command": [],
                "command_group": [],
            },
            "credential_host": {
                "ssh_credential_host_id": [],
                "password_credential_host_id": [],
                "credential_group": []
            }
        }
        if self.strategy_command_user_or_user_group.get_queryset():
            user_list = []
            user_group_list = []
            for _query in self.strategy_command_user_or_user_group.get_queryset():
                if _query.user:
                    user_list.append(_query.user.id)
                if _query.user_group:
                    user_group_list.append(_query.user_group.id)
            if user_list:
                dt["user"].update({"user": user_list})
            if user_group_list:
                dt["user"].update({"user_group": user_group_list})
        if self.strategy_command_or_group.get_queryset():
            command_list = []
            command_group_list = []
            for _query in self.strategy_command_or_group.get_queryset():
                if _query.command:
                    command_list.append(_query.command.id)
                if _query.command_group:
                    command_group_list.append(_query.command_group.id)
            if command_list:
                dt["command"].update({"command": command_list})
            if command_group_list:
                dt["command"].update({"command_group": command_group_list})
        if self.new_strategy_command_credential_or_credential_group.get_queryset():
            ssh_credential_host = []
            password_credential_host = []
            credential_group = []
            for _query in self.new_strategy_command_credential_or_credential_group.get_queryset():
                if _query.credential_host:
                    if _query.credential_host.credential.credential_type == CredentialModel.CREDENTIAL_SSH_KEY:
                        ssh_credential_host.append(_query.credential_host.to_dict())
                    if _query.credential_host.credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                        password_credential_host.append(_query.credential_host.to_dict())
                if _query.credential_group:
                    credential_group.append(_query.credential_group.to_base_dict())
            dt["credential_host"].update({"ssh_credential_host_id": ssh_credential_host})
            dt["credential_host"].update({"password_credential_host_id": password_credential_host})
            dt["credential_host"].update({"credential_group": credential_group})
        return dt

    def to_list_dict(self):
        dt = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "start_time": str(self.start_time).rsplit(".", 1)[0] if self.start_time else "",
            "end_time": str(self.end_time).rsplit(".", 1)[0] if self.end_time else "",
            "create_time": str(self.create_time).rsplit(".", 1)[0] if self.create_time else "",
            "login_time_limit": self.get_list_field(self.login_time_limit) if self.get_list_field(
                self.login_time_limit) else self.DEFAULT_LOGIN_TIME,
            "user": {
                "user": [],
                "user_group": []
            },
            "command": {
                "command": [],
                "command_group": [],
            },
            "credential_host": {
                "ssh_credential_host_id": [],
                "password_credential_host_id": [],
                "credential_group": []
            }
        }
        if self.strategy_command_user_or_user_group.get_queryset():
            user_list = []
            user_group_list = []
            for _query in self.strategy_command_user_or_user_group.get_queryset():
                if _query.user:
                    user_list.append({"user_id": _query.user.id, "user_name": _query.user.username})
                if _query.user_group:
                    user_group_list.append(
                        {"user_group_id": _query.user_group.id, "user_group_name": _query.user_group.name})
            dt["user"].update({"user": user_list})
            dt["user"].update({"user_group": user_group_list})
        if self.strategy_command_or_group.get_queryset():
            command_list = []
            command_group_list = []
            for _query in self.strategy_command_or_group.get_queryset():
                if _query.command:
                    command_list.append({"command_id": _query.command.id})
                if _query.command_group:
                    command_group_list.append({"command_group_id": _query.command_group.id})
            dt["command"].update({"command": command_list})
            dt["command"].update({"command_group": command_group_list})
        if self.new_strategy_command_credential_or_credential_group.get_queryset():
            ssh_credential_host = []
            password_credential_host = []
            credential_group = []
            for _query in self.new_strategy_command_credential_or_credential_group.get_queryset():
                if _query.credential_host:
                    if _query.credential_host.credential.credential_type == CredentialModel.CREDENTIAL_SSH_KEY:
                        ssh_credential_host.append({"credential_host_id": _query.credential_host.id})
                    if _query.credential_host.credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                        password_credential_host.append({"credential_host_id": _query.credential_host.id})
                if _query.credential_group:
                    credential_group.append({"credential_group_id": _query.credential_group.id})
            dt["credential_host"].update({"ssh_credential_host_id": ssh_credential_host})
            dt["credential_host"].update({"password_credential_host_id": password_credential_host})
            dt["credential_host"].update({"credential_group": credential_group})
        return dt


# 命令策略关联命令，命令分组
class StrategyCommandGroupRelationshipModel(BaseModel):
    strategy_command = models.ForeignKey(StrategyCommandModel, on_delete=models.CASCADE, verbose_name="命令策略",
                                         related_name="strategy_command_or_group")
    command = models.ForeignKey(CommandModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="命令",
                                related_name="command_strategy")
    command_group = models.ForeignKey(CommandGroupModel, on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name="命令分组", related_name="command_group_strategy")

    class Meta:
        db_table = "strategy_command_group_relationship"
        verbose_name = "命令策略关联命令，命令分组"
        verbose_name_plural = verbose_name

    def to_dict(self):
        dic = {
            "id": self.id,
            "strategy": self.strategy_command.to_dict(),
            "command": self.command.to_dict(),
            "command_group": self.command_group.to_dict(),
        }
        return dic


# 命令策略关联用户，用户分组
class StrategyCommandUserGroupRelationshipModel(BaseModel):
    strategy_command = models.ForeignKey(StrategyCommandModel, on_delete=models.CASCADE, verbose_name="关联策略",
                                         related_name="strategy_command_user_or_user_group")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank=True, verbose_name="用户",
                             related_name="user_strategy_command")
    user_group = models.ForeignKey(UserGroupModel, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="用户组", related_name="user_group_strategy_command")

    class Meta:
        db_table = "strategy_command_user_group_relationship"
        verbose_name = "命令策略关联用户，用户组"
        verbose_name_plural = verbose_name

    def to_dict(self):
        dic = {
            "id": self.id,
            "strategy": self.strategy_command.to_dict(),
            "user": self.user.to_dict(),
            "user_group": self.user_group.to_dict(),
        }
        return dic


# 凭据分组
class CredentialGroupModel(BaseModel):
    name = models.CharField(max_length=100, verbose_name="分组名称")
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name="描述")
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    class Meta:
        db_table = "credential_group"
        verbose_name = "凭据分组"
        verbose_name_plural = verbose_name

    def to_base_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "create_time": str(self.create_time).rsplit(".")[0],
        }
        return dic

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "create_time": str(self.create_time).rsplit(".")[0],
            "credential": self.get_base_ssh_password_credential_list(),
        }
        if self.get_base_host_list():
            dic["host_list"] = self.get_base_host_list()
        if self.user:
            dic["user"] = self.user.to_base_dict()
        return dic

    def to_all_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "create_time": str(self.create_time).rsplit(".")[0],
            "credential": self.get_ssh_password_credential_list(),
        }
        if self.user:
            dic["user"] = self.user.to_base_dict()
        if self.get_host_list():
            dic["host_list"] = self.get_host_list()
        return dic

    def get_base_host_list(self):
        credential_group_queryset = self.credential_group_host.get_queryset()
        host_list = [credential_group_host.host.to_base_dict() for credential_group_host in credential_group_queryset]
        return host_list

    def get_base_ssh_password_credential_list(self):
        credential_group_queryset = self.credential_group_queryset.get_queryset()
        password_credential, ssh_credential = list(), list()
        for credential_group in credential_group_queryset:
            if credential_group.credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                password_credential.append(credential_group.credential.to_base_dict())
            if credential_group.credential.credential_type == CredentialModel.CREDENTIAL_SSH_KEY:
                ssh_credential.append(credential_group.credential.to_base_dict())
        return {"password_credential": password_credential, "ssh_credential": ssh_credential}

    def get_host_list(self):
        credential_group_queryset = self.credential_group_host.get_queryset()
        host_list = [credential_group_host.host.to_dict() for credential_group_host in credential_group_queryset]
        return host_list

    def get_ssh_password_credential_list(self):
        credential_group_queryset = self.credential_group_queryset.get_queryset()
        password_credential, ssh_credential = list(), list()
        for credential_group in credential_group_queryset:
            if credential_group.credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                password_credential.append(credential_group.credential.to_dict())
            if credential_group.credential.credential_type == CredentialModel.CREDENTIAL_SSH_KEY:
                ssh_credential.append(credential_group.credential.to_dict())
        return {"password_credential": password_credential, "ssh_credential": ssh_credential}


# 凭据
class CredentialModel(BaseModel):
    LOGIN_AUTO = "auto"
    LOGIN_HAND = "hand"
    CREDENTIAL_PASSWORD = "password"
    CREDENTIAL_SSH_KEY = "ssh_key"
    LOGIN_TYPE = [(LOGIN_AUTO, '自动登录'), (LOGIN_HAND, '手动登录')]
    CREDENTIAL_TYPE = [(CREDENTIAL_PASSWORD, '密码凭据'), (CREDENTIAL_SSH_KEY, 'SSH秘钥')]
    name = models.CharField(max_length=100, verbose_name="凭据名称")
    login_type = models.CharField(max_length=20, choices=LOGIN_TYPE, default=LOGIN_AUTO, verbose_name="登录方式")
    credential_type = models.CharField(max_length=20, choices=CREDENTIAL_TYPE, default=CREDENTIAL_PASSWORD,
                                       verbose_name="凭据类型")
    credential_group = models.ForeignKey(CredentialGroupModel, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name="凭据分组")
    login_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="资源账户")
    login_password = models.CharField(max_length=500, null=True, blank=True, verbose_name="密码")
    ssh_key = models.TextField(null=True, blank=True, verbose_name="SSH Key")
    passphrase = models.CharField(max_length=500, null=True, blank=True, verbose_name="通行码")
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name="描述")
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    class Meta:
        db_table = "credential"
        verbose_name = "凭据"
        verbose_name_plural = verbose_name

    def to_base_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "login_type": self.login_type,
            "credential_type": self.credential_type,
            "login_name": self.login_name,
            "description": self.description,
        }
        return dic

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "login_type": self.login_type,
            "credential_type": self.credential_type,
            "login_name": self.login_name,
            "description": self.description,
            "create_time": str(self.create_time).rsplit(".")[0]
        }
        if self.get_credential_group():
            dic["credential_group"] = self.get_credential_group()
        if self.get_host_list:
            dic.update({"host_list": self.get_host_list()})
        return dic

    def get_credential_group(self):
        """获取当前凭据关联的全部分组"""
        credential_group_queryset = self.credential_queryset.get_queryset()
        credential_group = [credential_group.credential_group.to_base_dict() for credential_group in
                            credential_group_queryset]
        return credential_group

    def get_host_list(self):
        # credential_queryset = self.credential_host.get_queryset()
        credential_queryset = HostCredentialRelationshipModel.fetch_all(credential=self, credential_group__isnull=True)
        host_list = [credential_host.host.to_base_dict() for credential_host in credential_queryset]
        return host_list


# 凭据，凭据分组关联表
class CredentialGroupRelationshipModel(BaseModel):
    credential = models.ForeignKey(CredentialModel, on_delete=models.CASCADE, related_name="credential_queryset",
                                   verbose_name="关联凭据")
    credential_group = models.ForeignKey(CredentialGroupModel, on_delete=models.CASCADE,
                                         related_name="credential_group_queryset", null=True, verbose_name="关联凭据分组")

    class Meta:
        db_table = "credential_group_relationship"
        verbose_name = "凭据，凭据分组关联表"
        verbose_name_plural = verbose_name
        unique_together = (("credential", "credential_group"),)

    def to_dict(self):
        dic = {
            "id": self.id,
            "credential": self.credential.to_base_dict(),
            "credential_group": self.credential_group.to_base_dict(),
            "create_time": str(self.create_time).rsplit(".")[0]
        }
        return dic


# 凭据凭据分组关联访问策略
class CredentialGroupStrategyAccessRelationshipModel(BaseModel):
    strategy_access = models.ForeignKey(StrategyAccessModel, on_delete=models.CASCADE, verbose_name="关联策略",
                                        related_name="strategy_access_credential_or_credential_group")
    credential = models.ForeignKey(CredentialModel, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="关联凭证", related_name="credential_strategy_access")
    credential_group = models.ForeignKey(CredentialGroupModel, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name="关联凭证分组", related_name="credential_group_strategy_access")

    class Meta:
        db_table = "credential_Group_strategy_access_relationship"
        verbose_name = "凭据凭据分组关联访问策略"
        verbose_name_plural = verbose_name

    def to_dict(self):
        dic = {
            "id": self.id,
            "strategy_access": self.strategy_access.to_dict(),
            "credential": self.credential.to_dict(),
            "credential_group": self.credential_group.to_dict(),
        }
        return dic


# 凭据凭据分组关联命令策略
class CredentialGroupStrategyCommandRelationshipModel(BaseModel):
    strategy_command = models.ForeignKey(StrategyCommandModel, on_delete=models.CASCADE, verbose_name="关联策略",
                                         related_name="strategy_command_credential_or_credential_group")
    credential = models.ForeignKey(CredentialModel, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="关联凭证", related_name="credential_strategy_command")
    credential_group = models.ForeignKey(CredentialGroupModel, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name="关联凭证分组", related_name="credential_group_strategy_command")

    class Meta:
        db_table = "credential_Group_strategy_command_relationship"
        verbose_name = "凭据凭据分组关联命令策略"
        verbose_name_plural = verbose_name

    def to_dict(self):
        dic = {
            "id": self.id,
            "strategy": self.strategy_command.to_dict(),
            "credential": self.credential.to_dict(),
            "credential_group": self.credential_group.to_dict(),
        }
        return dic


# 主机分组
class HostGroupModel(BaseModel):
    RESOURCE_HOST = "host"
    RESOURCE_DATABASE = "database"
    RESOURCE_TYPE = [(RESOURCE_HOST, "主机资源"), (RESOURCE_DATABASE, "数据库")]
    name = models.CharField(max_length=100, verbose_name="主机分组名称")
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name="描述")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children_group",
                               verbose_name="上级")
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")
    # host databases
    group_type = models.CharField(max_length=20, choices=RESOURCE_TYPE, default=RESOURCE_HOST, verbose_name="主机分组类型")

    class Meta:
        db_table = "host_group"
        verbose_name = "主机分组"
        verbose_name_plural = verbose_name

    def to_base_dict(self):
        dic = {
            "id": self.id,
            "name": self.name
        }
        return dic

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "group_type": self.group_type,
            "create_time": str(self.create_time).rsplit(".")[0]
        }
        if self.get_host_list():
            dic["host"] = self.get_host_list()
        return dic

    def to_parent_dict(self, user_query=None):
        children = []
        children_query_set = HostGroupModel.fetch_all(parent=self).order_by("create_time")
        for i in children_query_set:
            children.append(i.to_parent_dict(user_query))
        dic = {
            "id": self.id,
            "name": self.name,
            "create_time": str(self.create_time).rsplit(".")[0],
            "children": children
        }
        if self.get_host_list():
            dic["host"] = True
        else:
            dic["host"] = False
        if user_query:
            dic["count"] = self.get_group_resource_count(user_query)
        else:
            dic["count"] = 0
        return dic

    def get_group_resource_count(self, user_query):
        resource_count = 0
        if user_query.role == 1:
            kwargs = {"resource_type": self.group_type}
            kwargs["group__in"] = self.get_children_group_queryset() + [self]
            resource_count = HostModel.fetch_all(**kwargs).count()
        else:
            resource_queryset = user_query.get_user_host_queryset_v3()
            for resource_query in resource_queryset:
                if resource_query.group == self:
                    if resource_query.resource_type == self.group_type:
                        resource_count += 1
        return resource_count

    def to_parent_host_dict(self, **kwargs):
        children = []
        children_query_set = HostGroupModel.fetch_all(parent=self, **kwargs).order_by("create_time")
        for i in children_query_set:
            children.append(i.to_parent_host_dict())
        dic = {
            "id": self.id,
            "name": self.name,
            "create_time": str(self.create_time).rsplit(".")[0],
            "host": 1,
            "children": children
        }
        if self.get_host_list():
            dic["host"] = self.get_host_list()
        return dic

    def get_host_list(self):
        host_group_queryset = self.host_group.get_queryset()
        return [host.to_dict() for host in host_group_queryset]

    def check_host_dict(self):
        host_query = HostModel.fetch_one(group=self)
        if host_query:
            return True
        children_query_set = HostGroupModel.fetch_all(parent=self)
        for children_query in children_query_set:
            children_host_query = HostModel.fetch_one(group=children_query)
            if children_host_query:
                return True
            else:
                return children_query.check_host_dict()
        return False

    def get_children_group_queryset(self):
        children_group_queryset = list()
        query_set = HostGroupModel.fetch_all(parent=self)
        children_group_queryset.extend(query_set)
        for children_query in query_set:
            children_query_set = HostGroupModel.fetch_all(parent=children_query)
            children_group_queryset.extend(children_query_set)
            if children_query_set:
                children_group_queryset += children_query.get_children_group_queryset()

        return list(set(children_group_queryset))

    def get_access_host(self, user_query=None, search_data=None):
        if search_data:
            host_queryset_host_name = HostModel.fetch_all(group=self, host_name__contains=search_data)
            host_queryset_host_address = HostModel.fetch_all(group=self, host_address__contains=search_data)
            host_queryset = list(host_queryset_host_name) + list(host_queryset_host_address)
        else:
            host_queryset = self.host_group.get_queryset()
        if user_query:
            host_queryset = user_query.get_user_host_in_group(self, search_data)
        return [host.to_console_dict() for host in host_queryset]

    def to_all_dict(self, user_query=None, search_data=None):
        dt = {
            "id": self.id,
            "name": self.name,
            "group_type": self.group_type,
            "key": "group_" + str(self.id),
            "type": "group",
        }
        children = []
        host_query = self.get_access_host(user_query, search_data)
        if host_query:
            children = host_query
        if self.children_group.get_queryset():
            children = [children.to_all_dict(user_query, search_data) for children in
                        self.children_group.get_queryset()]
            children.extend(self.get_access_host(user_query, search_data))
        dt["children"] = children
        return dt

    def to_all_v2_dict(self, user_query=None):
        dt = {
            "id": self.id,
            "name": self.name,
            "key": "group_" + str(self.id),
            "type": "group",
        }
        children = []
        children.extend(self.get_access_host(user_query))
        if self.children_group.get_queryset():
            children = [children.to_all_dict() for children in self.children_group.get_queryset()]
        dt["children"] = children

        return dt


class NetworkProxyModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name="网路代理名称")
    linux_ip = models.CharField(max_length=150, null=True, blank=True, verbose_name="Linux IP地址")
    linux_port = models.IntegerField(default=22, null=True, blank=True, verbose_name="Linux端口")
    linux_login_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Linux登录名")
    linux_login_password = models.CharField(max_length=500, null=True, blank=True, verbose_name="Linux密码")
    windows_ip = models.CharField(max_length=150, null=True, blank=True, verbose_name="Windows IP地址")
    windows_port = models.IntegerField(default=22, null=True, blank=True, verbose_name="Windows端口")
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name="网路代理描述")
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    class Meta:
        db_table = "network_proxy"
        verbose_name = "网络代理"
        verbose_name_plural = verbose_name

    def to_base_dict(self):
        dic = {
            "id": self.id,
            "name": self.name
        }
        return dic

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "linux_ip": self.linux_ip,
            "linux_port": self.linux_port,
            "linux_login_name": self.linux_login_name,
            "linux_login_password": self.linux_login_password,
            "windows_ip": self.windows_ip,
            "windows_port": self.windows_port,
            "user": self.user.to_base_dict(),
            "description": self.description,
        }
        if HostModel.fetch_all(network_proxy=self):
            dic["resource"] = True
        else:
            dic["resource"] = False
        return dic


# 主机资源
class HostModel(BaseModel):
    # DATABASES_MYSQL = "MySQL"
    # DATABASES_MongoDB = "MongoDB"
    # DATABASES_Redis = "Redis"
    # DATABASES_TYPE = [(DATABASES_MYSQL, "MYSQL"), (DATABASES_MongoDB, "MongoDB"), (DATABASES_Redis, "Redis")]
    SYSTEM_LINUX = "Linux"
    SYSTEM_WINDOWS = "Windows"
    PROTOCOL_SSH = "SSH"
    PROTOCOL_RDP = "RDP"
    PROTOCOL_TELNET = "Telnet"
    PROTOCOL_VNC = "VNC"
    SYSTEM_TYPE = [(SYSTEM_LINUX, 'Linux'), (SYSTEM_WINDOWS, 'Windows')]
    PROTOCOL_TYPE = [(PROTOCOL_SSH, 'SSH'), (PROTOCOL_RDP, 'RDP'), (PROTOCOL_TELNET, 'Telnet'), (PROTOCOL_VNC, 'VNC')]
    RESOURCE_HOST = "host"
    RESOURCE_DATABASE = "database"
    RESOURCE_TYPE = [(RESOURCE_HOST, "主机资源"), (RESOURCE_DATABASE, "数据库")]

    host_name_code = models.CharField(max_length=200, default="", verbose_name="主机唯一标识")
    host_name = models.CharField(max_length=100, verbose_name="主机名称")
    # mysql mongodb redis
    database_type = models.CharField(max_length=20, null=True, blank=True, verbose_name="数据库类型")
    system_type = models.CharField(max_length=20, choices=SYSTEM_TYPE, default=SYSTEM_LINUX, verbose_name="系统类型")
    protocol_type = models.CharField(max_length=20, choices=PROTOCOL_TYPE, default=PROTOCOL_SSH, verbose_name="协议类型")
    host_address = models.CharField(max_length=150, verbose_name="主机地址")
    # hand 手动添加 cmdb 资源平台添加 cmdb_batch 资源批量添加 excel_batch 表格批量添加
    resource_from = models.CharField(max_length=30, default="hand", null=True, blank=True, verbose_name="数据来源")
    port = models.IntegerField(default=22, verbose_name="端口")
    group = models.ForeignKey(HostGroupModel, on_delete=models.CASCADE, related_name="host_group", verbose_name="所属分组")
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")
    description = models.CharField(max_length=3000, null=True, blank=True, verbose_name="主机描述")
    # host database
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE, default=RESOURCE_HOST, verbose_name="资源类型")
    network_proxy = models.ForeignKey(NetworkProxyModel, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name="network_proxy")

    class Meta:
        db_table = "host"
        verbose_name = "主机资源"
        verbose_name_plural = verbose_name

    def to_base_dict(self):
        dic = {
            "id": self.id,
            "host_name": self.host_name,
            "host_name_code": self.host_name_code,
            "host_address": self.host_address,
            "resource_type": self.resource_type,
            "create_time": str(self.create_time).rsplit(".")[0]
        }
        if self.network_proxy:
            dic["network_proxy"] = self.network_proxy.to_base_dict()
        if self.resource_type == self.RESOURCE_HOST:
            dic["system_type"] = self.system_type
            dic["protocol_type"] = self.protocol_type
        elif self.resource_type == self.RESOURCE_DATABASE:
            dic["database_type"] = self.database_type
        return dic

    def to_dict(self):
        dic = {
            "id": self.id,
            "host_name": self.host_name,
            "host_name_code": self.host_name_code,
            "host_address": self.host_address,
            "resource_from": self.resource_from,
            "port": self.port,
            "group": self.group.to_base_dict(),
            "resource_type": self.resource_type,
            "description": self.description,
            "create_time": str(self.create_time).rsplit(".")[0],
            "credential": self.get_base_credential_or_credential_group()
        }
        if self.user:
            dic["user"] = self.user.to_base_dict()
        if self.network_proxy:
            dic["network_proxy"] = self.network_proxy.to_base_dict()
        if self.resource_type == self.RESOURCE_HOST:
            dic["system_type"] = self.system_type
            dic["protocol_type"] = self.protocol_type
        elif self.resource_type == self.RESOURCE_DATABASE:
            dic["database_type"] = self.database_type
        return dic

    def to_network_proxy_dict(self):
        dic = {
            "id": self.id,
            "host_name": self.host_name,
            "host_name_code": self.host_name_code,
            "host_address": self.host_address,
            "resource_type": self.resource_type,
            "description": self.description,
        }
        if self.resource_type == self.RESOURCE_HOST:
            dic["system_type"] = self.system_type
            dic["protocol_type"] = self.protocol_type
        elif self.resource_type == self.RESOURCE_DATABASE:
            dic["database_type"] = self.database_type
        return dic

    def to_auth_host_dict(self):
        dic = {
            "id": self.id,
            "host_name": self.host_name,
            "host_name_code": self.host_name_code,
            "host_address": self.host_address,
            "port": self.port,
            "resource_type": self.resource_type,
            "group": self.group.to_base_dict(),
            "create_time": str(self.create_time).rsplit(".")[0],
        }
        if self.network_proxy:
            dic["network_proxy"] = self.network_proxy.to_base_dict()
        if self.resource_type == self.RESOURCE_HOST:
            dic["system_type"] = self.system_type
            dic["protocol_type"] = self.protocol_type
        elif self.resource_type == self.RESOURCE_DATABASE:
            dic["database_type"] = self.database_type
        return dic

    def to_console_dict(self):
        dic = {
            "id": self.id,
            "name": self.host_name,
            "host_name": self.host_name,
            "host_name_code": self.host_name_code,
            "host_address": self.host_address,
            "resource_from": self.resource_from,
            "type": "host",
            "key": "host_" + str(self.id),
            "port": self.port,
            "group": self.group.to_base_dict(),
            "resource_type": self.resource_type,
            "description": self.description,
            "create_time": str(self.create_time).rsplit(".")[0],
        }
        if self.network_proxy:
            dic["network_proxy"] = self.network_proxy.to_base_dict()
        if self.resource_type == self.RESOURCE_HOST:
            dic["system_type"] = self.system_type
            dic["protocol_type"] = self.protocol_type
        elif self.resource_type == self.RESOURCE_DATABASE:
            dic["database_type"] = self.database_type
        return dic

    def get_all_dict(self):
        dic = {
            "id": self.id,
            "host_name": self.host_name,
            "host_name_code": self.host_name_code,
            # "system_type": self.system_type,
            # "protocol_type": self.protocol_type,
            "host_address": self.host_address,
            "resource_from": self.resource_from,
            "port": self.port,
            "group": self.group.to_base_dict(),
            "resource_type": self.resource_type,
            "description": self.description,
            "create_time": str(self.create_time).rsplit(".")[0],
            "credential": self.get_base_credential_or_credential_group()
        }
        if self.network_proxy:
            dic["network_proxy"] = self.network_proxy.to_base_dict()
        if self.resource_type == self.RESOURCE_HOST:
            dic["system_type"] = self.system_type
            dic["protocol_type"] = self.protocol_type
        elif self.resource_type == self.RESOURCE_DATABASE:
            dic["database_type"] = self.database_type
        if self.user:
            dic["user"] = self.user.to_base_dict()
        return dic

    def get_base_credential_or_credential_group(self):
        credential_or_credential_group = dict()
        password_credential_list, ssh_credential_list, credential_group_list = list(), list(), list()
        for _query in self.host_credential_or_credential_group.get_queryset():
            if _query.credential and not _query.credential_group:
                if _query.credential.credential_type == _query.credential.CREDENTIAL_SSH_KEY:
                    ssh_credential_list.append(_query.credential.to_base_dict())
                if _query.credential.credential_type == _query.credential.CREDENTIAL_PASSWORD:
                    password_credential_list.append(_query.credential.to_base_dict())
            if _query.credential_group:
                if _query.credential_group.to_base_dict() not in credential_group_list:
                    credential_group_list.append(_query.credential_group.to_base_dict())
        if password_credential_list:
            credential_or_credential_group["password_credential"] = password_credential_list
        if ssh_credential_list:
            credential_or_credential_group["ssh_credential"] = ssh_credential_list
        if credential_group_list:
            credential_or_credential_group["credential_group"] = credential_group_list
        return credential_or_credential_group

    def get_all_credential_queryset(self):
        credential_queryset = list()
        for _query in self.host_credential_or_credential_group.get_queryset():
            if _query.credential:
                credential_queryset.append(_query.credential)
            if _query.credential_group:
                for credential_group in _query.credential_group.credential_group_queryset.get_queryset():
                    credential_queryset.append(credential_group.credential)
        return credential_queryset


# 主机与凭据，凭据组关联
class HostCredentialRelationshipModel(BaseModel):
    host = models.ForeignKey(HostModel, related_name="host_credential_or_credential_group", on_delete=models.CASCADE)
    credential = models.ForeignKey(CredentialModel, on_delete=models.CASCADE, related_name="credential_host", null=True,
                                   blank=True)
    # 前端回显
    credential_group = models.ForeignKey(CredentialGroupModel, on_delete=models.CASCADE,
                                         related_name="credential_group_host", null=True, blank=True)
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    class Meta:
        db_table = "host_credential_relationship"
        verbose_name = "主机与凭据，凭据组关联"
        verbose_name_plural = verbose_name
        unique_together = (("host", "credential", "credential_group"),)

    def to_dict(self):
        dic = {
            "id": self.id,
            "host": self.host.to_dict()
        }
        if self.credential:
            dic["credential"] = self.credential.to_base_dict()
        if self.credential_group:
            dic["credential_group"] = self.credential_group.to_base_dict()
        return dic

    def to_base_dict(self):
        dt = {
            "id": self.id,
            "host_name": self.host.host_name,
            "credential_name": self.credential.name,
            "host_address": self.host.host_address,
            "credential_type": self.credential.credential_type,
            "login_type": self.credential.login_type,
            "login_name": self.credential.login_name
        }
        return dt


# 操作日志
class OperationLogModel(BaseModel):
    username = models.CharField(max_length=100, verbose_name="操作人用户名")
    operation_type = models.CharField(max_length=50, verbose_name="操作类型")
    operation_object = models.CharField(max_length=100, verbose_name="操作对象")
    operation_content = models.CharField(max_length=5000, verbose_name="操作内容")
    parameter = models.TextField(null=True, blank=True, verbose_name="参数")
    method = models.CharField(max_length=20, null=True, blank=True, verbose_name="请求方式")

    class Meta:
        db_table = "operation_log"
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name

    def to_dict(self):
        dic = {
            "id": self.id,
            "username": self.username,
            "operation_type": self.operation_type,
            "operation_object": self.operation_object,
            "operation_content": self.operation_content,
            "parameter": self.parameter,
            "method": self.method,
            "create_time": str(self.create_time).rsplit(".")[0]
        }
        return dic


# 会话日志
class SessionLogModel(BaseModel):
    host = models.ForeignKey(HostModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="主机")
    channel = models.CharField(max_length=100, verbose_name="通道名", blank=False, unique=True, editable=False)
    log_name = models.CharField(max_length=100, verbose_name="日志名", blank=False, unique=False, editable=False)
    host_name = models.CharField(max_length=100, verbose_name="主机名称", blank=True, null=True)
    system_type = models.CharField(max_length=100, verbose_name="系统类型", default="Linux")
    host_address = models.CharField(max_length=100, verbose_name="主机地址", blank=True, null=True)
    port = models.IntegerField(default=22, verbose_name="端口")
    protocol_type = models.CharField(max_length=20, blank=True, null=True, verbose_name="协议类型")
    login_name = models.CharField(max_length=100, verbose_name="系统用户", blank=True, null=True)
    # 1 正常登陆     2 临时登陆
    login_type = models.IntegerField(default=1)
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="开始时间")
    end_time = models.DateTimeField(auto_created=True, auto_now=True, verbose_name="结束时间")
    is_finished = models.BooleanField(default=False, verbose_name="是否完成")
    user = models.CharField(max_length=100, verbose_name="用户名", blank=False, unique=False)
    width = models.PositiveIntegerField(default=1024, verbose_name="宽度")
    height = models.PositiveIntegerField(default=768, verbose_name="高度")
    guacamole_client_id = models.CharField(max_length=100, verbose_name="Gucamole通道名称", blank=True, editable=False)
    # TAG CHOICE: [init, connect]
    tag = models.CharField(max_length=100, verbose_name="标签", blank=True, null=True)

    class Meta:
        db_table = "session_log"
        verbose_name = "会话日志"
        verbose_name_plural = verbose_name
        ordering = [
            ('-start_time')
        ]

    def to_dict(self):
        dt = {
            "id": self.id,
            "channel": self.channel,
            "log_name": self.log_name,
            "host_name": self.host_name,
            "system_type": self.system_type,
            "port": self.port,
            "protocol_type": self.protocol_type,
            "host_address": self.host_address,
            "login_name": self.login_name,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "is_finished": self.is_finished,
            "user": self.user,
        }
        if self.host:
            dt["host_name"] = self.host.host_name
            dt["system_type"] = self.host.system_type
            dt["host_address"] = self.host.host_address
            dt["port"] = self.host.port
            dt["protocol_type"] = self.host.protocol_type

        return dt


class SessionCommandHistoryModel(BaseModel):
    session_log = models.ForeignKey(SessionLogModel, on_delete=models.CASCADE)
    command = models.TextField()

    class Meta:
        db_table = "session_command_history"

    def to_dict(self):
        return {
            "id": self.id,
            "session_log_id": self.session_log.id,
            "command": self.command,
            "create_time": str(self.create_time).rsplit(".", 1)[0],
        }


# 命令日志
class CommandLogModel(BaseModel):
    command = models.CharField(max_length=255, verbose_name="指令")
    block_type = models.CharField(max_length=8, null=True, verbose_name="阻断类型")
    intercept_command = models.CharField(max_length=255, null=True)
    status_choice = [('y', '执行'), ('n', '未执行')]
    status = models.CharField(max_length=8, choices=status_choice, default='n', verbose_name="指令是否执行")
    hostname = models.CharField(max_length=255, verbose_name="服务器IP")
    user = models.CharField(max_length=32, null=True, verbose_name="用户名")
    opt_user = models.CharField(max_length=32, null=True, verbose_name="操作用户")

    class Meta:
        db_table = "command_log"
        verbose_name = "命令日志"
        verbose_name_plural = verbose_name
        ordering = [
            ('-create_time')
        ]

    def __unicode__(self):
        return self.command

    def __str__(self):
        return self.command

    def to_dict(self):
        return {
            "id": self.id,
            "block_type": self.block_type,
            "intercept_command": self.intercept_command,
            "command": self.command,
            "status": self.status,
            "hostname": self.hostname,
            "user": self.user,
            "opt_user": self.opt_user,
            "create_time": str(self.create_time).rsplit(".", 1)[0],
        }


# 访问策略关联   凭据与主机的中间关系   替代CredentialGroupStrategyAccessRelationshipModel
class StrategyAccessCredentialHostModel(BaseModel):
    strategy_access = models.ForeignKey(StrategyAccessModel, on_delete=models.CASCADE, verbose_name="关联策略",
                                        related_name="new_strategy_access_credential_or_credential_group")
    credential_group = models.ForeignKey(CredentialGroupModel, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name="关联凭证分组", related_name="new_credential_group_strategy_access")
    credential_host = models.ForeignKey(HostCredentialRelationshipModel, on_delete=models.CASCADE, null=True,
                                        related_name="new_credential_host_strategy_access")

    def to_dict(self):
        dt = {
            "id": self.id,
        }
        if self.credential_host:
            dt["credential_host"] = self.credential_host.to_base_dict()
        if self.credential_group:
            dt["credential_group"] = self.credential_group.to_base_dict()
        return dt


# 命令策略关联   凭据与主机的中间关系      替代CredentialGroupStrategyCommandRelationshipModel
class StrategyCommandCredentialHostModel(BaseModel):
    strategy_command = models.ForeignKey(StrategyCommandModel, on_delete=models.CASCADE, verbose_name="关联策略",
                                         related_name="new_strategy_command_credential_or_credential_group")
    credential_host = models.ForeignKey(HostCredentialRelationshipModel, on_delete=models.CASCADE, null=True,
                                        related_name="new_credential_strategy_command")
    credential_group = models.ForeignKey(CredentialGroupModel, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name="关联凭证分组", related_name="new_credential_group_strategy_command")

    def to_dict(self):
        dt = {
            "id": self.id,
        }
        if self.credential_host:
            dt["credential_host"] = self.credential_host.to_base_dict()
        if self.credential_group:
            dt["credential_group"] = self.credential_group.to_base_dict()
        return dt
