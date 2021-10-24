import os
import re
import json
from django.http import JsonResponse, HttpResponse
import uuid
from django_redis import get_redis_connection
import datetime
import logging
import paramiko
import settings
import io

from bastion.forms.core_form import LinkCheckForm, LinkCheckV2Form, GetCacheTokenForm
from bastion.forms import first_error_message
from bastion.models import HostModel, UserInfo, CredentialModel, CredentialGroupRelationshipModel, \
    StrategyAccessModel, UserGroupRelationshipModel, StrategyAccessUserGroupRelationshipModel, \
    CredentialGroupStrategyAccessRelationshipModel, StrategyCommandModel, StrategyCommandGroupRelationshipModel, \
    CredentialGroupStrategyCommandRelationshipModel, HostCredentialRelationshipModel, \
    StrategyAccessCredentialHostModel, UserGroupModel
from bastion.utils.status_code import success, error, SuccessStatusCode, ErrorStatusCode
from bastion.component.common import GetUserInfo
from bastion.utils.encryption import PasswordEncryption
from bastion.utils.esb_api import EsbApi

app_logging = logging.getLogger("app")


class CheckUserHostComponent:
    def get_user(self, token="", request=""):
        if token:
            user = GetUserInfo().get_user_info(bk_token=token)
        elif request:
            user = GetUserInfo().get_user_info(request=request)
        else:
            user = None
        return user is not None, user

    def get_user_all_strategy_access(self, user):
        """
        获取用户以及用户所在用户组所有的访问策略
        """
        user_group_rel_query_set = UserGroupRelationshipModel.fetch_all(user=user)
        user_group_query_set = [user_group_rel_query.user_group for user_group_rel_query in user_group_rel_query_set]
        user_access_strategy = StrategyAccessUserGroupRelationshipModel.fetch_all(user=user)
        user_group_access_strategy = StrategyAccessUserGroupRelationshipModel.fetch_all(
                user_group__in=user_group_query_set
        )
        access_strategy = []
        for _user_access_strategy in user_access_strategy:
            if _user_access_strategy.strategy_access not in access_strategy:
                access_strategy.append(_user_access_strategy.strategy_access)
        for _user_group_access_strategy in user_group_access_strategy:
            if _user_group_access_strategy.strategy_access not in access_strategy:
                access_strategy.append(_user_group_access_strategy.strategy_access)
        return access_strategy

    def get_user_all_strategy_command(self, user):
        """
        获取用户以及用户所在用户组所有的命令策略
        """
        user_group_rel_query_set = UserGroupRelationshipModel.fetch_all(user=user)
        user_group_query_set = [user_group_rel_query.user_group for user_group_rel_query in user_group_rel_query_set]
        user_command_strategy = StrategyCommandGroupRelationshipModel.fetch_all(user=user)
        user_group_command_strategy = StrategyCommandGroupRelationshipModel.fetch_all(
                user_group__in=user_group_query_set
        )
        access_strategy = []
        for _user_command_strategy in user_command_strategy:
            if _user_command_strategy.strategy_access not in access_strategy:
                access_strategy.append(_user_command_strategy.strategy_command)
        for _user_group_command_strategy in user_group_command_strategy:
            if _user_group_command_strategy.strategy_access not in access_strategy:
                access_strategy.append(_user_group_command_strategy.strategy_command)
        return access_strategy

    def get_credential_all_strategy_command(self, credential):
        """
        获取凭证以及凭证所在凭证组所有的命令策略
        """
        credential_group_rel_query_set = CredentialGroupRelationshipModel.fetch_all(credential=credential)
        credential_group_query_set = [credential_group_rel_query.credential_group
                                for credential_group_rel_query in credential_group_rel_query_set]
        credential_command_strategy = CredentialGroupStrategyCommandRelationshipModel.fetch_all(credential=credential)
        credential_group_command_strategy = CredentialGroupStrategyCommandRelationshipModel.fetch_all(
                credential_group__in=credential_group_query_set
        )
        command_strategy = []
        for _credential_command_strategy in credential_command_strategy:
            if _credential_command_strategy.strategy_command not in command_strategy:
                command_strategy.append(_credential_command_strategy.strategy_access)
        for _credential_group_command_strategy in credential_group_command_strategy:
            if _credential_group_command_strategy.command_strategy not in command_strategy:
                command_strategy.append(_credential_group_command_strategy.command_strategy)
        return command_strategy

    def get_credential_all_strategy_access(self, credential):
        """
        获取凭证以及凭证所在凭证组所有的访问策略
        """
        credential_group_rel_query_set = CredentialGroupRelationshipModel.fetch_all(credential=credential)
        credential_group_query_set = [credential_group_rel_query.credential_group
                                for credential_group_rel_query in credential_group_rel_query_set]
        credential_access_strategy = CredentialGroupStrategyAccessRelationshipModel.fetch_all(credential=credential)
        credential_group_access_strategy = CredentialGroupStrategyAccessRelationshipModel.fetch_all(
                credential_group__in=credential_group_query_set
        )
        access_strategy = []
        for _credential_access_strategy in credential_access_strategy:
            if _credential_access_strategy.strategy_access not in access_strategy:
                access_strategy.append(_credential_access_strategy.strategy_access)
        for _credential_group_access_strategy in credential_group_access_strategy:
            if _credential_group_access_strategy.strategy_access not in access_strategy:
                access_strategy.append(_credential_group_access_strategy.strategy_access)
        return access_strategy

    def get_valid_command_strategy(self, user, credential):
        # 不需要验证主机与凭证的关系，在LinkCheckForm中已经验证了主机与凭证的关系
        user_command_strategy = self.get_user_all_strategy_command(user)
        credential_command_strategy = self.get_credential_all_strategy_command(credential)
        command_strategy = []
        for _user_command_strategy in user_command_strategy:
            if _user_command_strategy in credential_command_strategy:
                command_strategy.append(_user_command_strategy)
        return command_strategy

    def get_valid_access_strategy(self, user, credential_host):
        # 不需要验证主机与凭证的关系，在LinkCheckForm中已经验证了主机与凭证的关系
        user_access_strategy = self.get_user_all_strategy_access(user)
        credential_access_strategy = self.get_credential_all_strategy_access(credential_host)
        access_strategy = []
        for _user_access_strategy in user_access_strategy:
            if _user_access_strategy in credential_access_strategy:
                access_strategy.append(_user_access_strategy)
        return access_strategy

    def get_time(self, strategy):
        start_time = strategy.get("start_time")
        end_time = strategy.get("end_time")
        if start_time and end_time:
            if start_time < datetime.datetime.now() < end_time:
                return True
            return False
        elif start_time:
            if start_time < datetime.datetime.now():
                return True
            return False
        elif end_time:
            if datetime.datetime.now() < end_time:
                return True
            return False
        else:
            return True

    def check_access_strategy(self, access_strategy=[], access_ip=""):
        flag = False
        week_day = datetime.datetime.now().isoweekday()
        hour = datetime.datetime.now().hour
        data = {
            "access_ip": access_ip,
            "login_time_limit": []
        }
        for _access_strategy in access_strategy:
            _access_strategy["status"] = True
            if _access_strategy.get("status") and self.get_time(_access_strategy):
                check_ip = False
                check_time = False
                # 验证黑白名单
                if _access_strategy.get("ip_limit") == 2:
                    try:
                        if access_ip not in _access_strategy.get("limit_list"):
                            check_ip = True
                    except Exception as e:
                        app_logging.error("[ERROR] Check IP black list error: {}, param: {}".format(
                                str(e), str(_access_strategy.id))
                        )
                elif _access_strategy.get("ip_limit") == 3:
                    try:
                        if access_ip in _access_strategy.get("limit_list"):
                            check_ip = True
                    except Exception as e:
                        app_logging.error("[ERROR] Check IP white list error: {}, param: {}".format(
                                str(e), str(_access_strategy.id))
                        )
                else:
                    check_ip = True
                # 验证访问时间
                if _access_strategy.get("login_time_limit"):
                    try:
                        for _login_time_limit in _access_strategy.get("login_time_limit"):
                            if _login_time_limit.get("week") == week_day:
                                if hour in _login_time_limit.get("time"):
                                    check_time = True
                        data["login_time_limit"] = _access_strategy.get("login_time_limit")
                    except Exception as e:
                        app_logging.error("[ERROR] Check time error: {}, param: {}".format(
                                str(e), str(_access_strategy.id))
                        )
                if check_ip and check_time:
                    flag = True
        return flag, data

    def check_user_strategy_access(self, user, credential, access_ip):
        """
        检查用户访问策略
        """
        if access_ip:
            access_strategy = self.get_valid_access_strategy(user, credential)
            access_data = []
            file_upload = False
            file_download = False
            file_manager = False
            copy_tool = False
            for _access_strategy in access_strategy:
                if _access_strategy.copy_tool:
                    copy_tool = True
                if _access_strategy.file_download:
                    file_download = True
                if _access_strategy.file_manager:
                    file_manager = True
                if _access_strategy.file_upload:
                    file_upload = True
                dt = _access_strategy.to_list_dict()
                dt["start_time"] = _access_strategy.start_time
                dt["end_time"] = _access_strategy.end_time
                access_data.append(dt)
            # if user.role == 1:
            #     return True, "", {
            #         "access_data": [],
            #         "command_data": [],
            #         "file_download": True,
            #         "file_upload": True,
            #         "file_manager": True,
            #         "copy_tool": True
            #     }
            status, data = self.check_access_strategy(access_data, access_ip)
            if status:
                # 获取命令内容写入缓存
                command_data = self.handle_command_strategy(self.get_command_strategy(credential))
                return True, "", {
                    "access_data": access_data,
                    "command_data": command_data,
                    "file_download": file_download,
                    "file_upload": file_upload,
                    "file_manager": file_manager,
                    "copy_tool": copy_tool
                }
            return False, "未能通过访问策略校验", {}
        return False, "未能通过访问策略校验", {}

    def get_credential_host_all_strategy_access(self, credential_host_query):
        """
        获取资源凭证所涉及的所有策略
        """
        if credential_host_query.credential_group:
            # 查询绑定改组的
            credential_group = credential_host_query.credential_group
            access_strategy_rel = credential_group.new_credential_group_strategy_access.get_queryset()
        else:
            access_strategy_rel = credential_host_query.new_credential_host_strategy_access.get_queryset()
        access_strategy = [_access_strategy_rel.strategy_access for _access_strategy_rel in access_strategy_rel]
        return access_strategy

    def get_valid_access_strategy_v2(self, user, credential_host):
        # 不需要验证主机与凭证的关系，在LinkCheckForm中已经验证了主机与凭证的关系
        user_access_strategy = self.get_user_all_strategy_access(user)
        credential_host_access_strategy = self.get_credential_host_all_strategy_access(credential_host)
        access_strategy = []
        for _user_access_strategy in user_access_strategy:
            if _user_access_strategy in credential_host_access_strategy:
                access_strategy.append(_user_access_strategy)
        return access_strategy

    def check_user_strategy_access_v2(self, user, credential_host, access_ip):
        """
        检查用户访问策略
        """
        if access_ip:
            access_strategy = self.get_valid_access_strategy_v2(user, credential_host)
            access_data = []
            file_upload = False
            file_download = False
            file_manager = False
            copy_tool = False
            for _access_strategy in access_strategy:
                if _access_strategy.copy_tool:
                    copy_tool = True
                if _access_strategy.file_download:
                    file_download = True
                if _access_strategy.file_manager:
                    file_manager = True
                if _access_strategy.file_upload:
                    file_upload = True
                dt = _access_strategy.to_list_dict()
                dt["start_time"] = _access_strategy.start_time
                dt["end_time"] = _access_strategy.end_time
                access_data.append(dt)
            if user.role == 1:
                return True, "", {
                    "admin": True
                }
            status, data = self.check_access_strategy(access_data, access_ip)
            if status:
                # 获取命令内容写入缓存
                command_data = self.handle_command_strategy(self.get_command_strategy_v2(credential_host))
                return True, "", {
                    "access_data": access_data,
                    "command_data": command_data,
                    "file_download": file_download,
                    "file_upload": file_upload,
                    "file_manager": file_manager,
                    "copy_tool": copy_tool
                }
            return False, "未能通过访问策略校验", {}
        return False, "未能通过访问策略校验", {}

    def get_access_ip(self, request):
        if request.META.get("HTTP_X_FORWARDED_FOR"):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip

    def handle_command_strategy(self, command_strategy):
        """
        处理命令策略
        """
        all_command = {}
        for _command_strategy in command_strategy:
            command_query = _command_strategy.strategy_command_or_group.get_queryset()
            for _command_query in command_query:
                if _command_query.command:
                    command_and_strategy_object = {
                            "command": _command_query.command, "strategy": _command_strategy
                        }
                    if _command_query.command.command in all_command:
                        command_strategy_list = all_command.get(_command_query.command.command, [])
                        if command_and_strategy_object not in command_strategy_list:
                            command_strategy_list.append(command_and_strategy_object)
                            all_command[_command_query.command.command] = command_strategy_list
                    else:
                        all_command[_command_query.command.command] = [command_and_strategy_object]
                if _command_query.command_group:
                    for _group_info in _command_query.command_group.command_group_queryset.get_queryset():
                        command_and_strategy_object = {
                           "command": _group_info.command, "strategy": _command_strategy
                        }
                        if _group_info.command.command in all_command:
                            command_strategy_list = all_command.get(_group_info.command.command, [])
                            if command_and_strategy_object not in command_strategy_list:
                                command_strategy_list.append(command_and_strategy_object)
                                all_command[_group_info.command.command] = command_strategy_list
                        else:
                            all_command[_group_info.command.command] = [command_and_strategy_object]
        return self.handle_all_command(all_command)

    def handle_command(self, command: str):
        """
        处理|,&,||,&&,;的情况
        ls | rm && cp; ls
        ls && rm
        """
        command_list = [command]
        flag_list = ["|", "&", ";"]

        def get_status(flag_list, command):
            for flag in flag_list:
                if flag in command:
                    return True
            return False

        while get_status(flag_list, command):
            for command in command_list:
                command_index = command_list.index(command)
                for flag in flag_list:
                    if flag in command:
                        command = command_list.pop(command_index)
                        res = command.split(flag)
                        for _res in res:
                            if _res:
                                command_list.insert(command_index, _res.strip())
        command_list.reverse()
        return command_list

    def check_time(self, start_time, end_time, check_time):
        if start_time or end_time:
            if start_time and end_time:
                if start_time < check_time < end_time:
                    return True
                return False
            elif start_time and not end_time:
                if start_time < check_time:
                    return True
                return False
            elif not start_time and end_time:
                if check_time < end_time:
                    return True
                return False
            else:
                return False
        return True

    def check_command(self, info={}, command="", token=""):
        if token:
            try:
                data = get_redis_connection("cache").get(token).decode("utf-8")
                data = eval(data)
                if data.get("admin") or data.get("cache"):
                    return True, 0, {}
                info = data.get("command_data")
            except Exception as e:
                app_logging.error("[ERROR] Check command, check_command error: {}, param: {}".format(
                        str(e), str(command) + " " + str(token))
                )
                info = {}
        flag = True
        level = 0
        message = {}
        current_time = datetime.datetime.now()
        # current_time = datetime.datetime.strptime("2021-08-31T13:06:24", "%Y-%m-%dT%H:%M:%S")
        week_day = current_time.isoweekday()
        hour = current_time.hour
        command_list = self.handle_command(command)
        app_logging.debug("[DEBUG] Check command, check_command {}, {}".format(command, token))
        for _command in command_list:
            if info.get(_command):
                for strategy in info.get(_command):
                    start_time = strategy.get("start_time")
                    end_time = strategy.get("end_time")
                    login_time_limit = strategy.get("login_time_limit")
                    block_type = strategy.get("block_type")
                    block_info = strategy.get("block_info")
                    if self.check_time(start_time, end_time, current_time):
                        for _login_time_limit in login_time_limit:
                            if _login_time_limit.get("week") == week_day:
                                if hour not in _login_time_limit.get("time"):
                                    flag = False
                                    if level:
                                        if level != 1:
                                            level = block_type
                                            message[_command] = block_info
                                    else:
                                        level = block_type
                                        message[_command] = block_info
                                    if block_type == 1:
                                        message[_command] = block_info
        return flag, level, message

    def handle_all_command(self, all_command):
        """
            {
                'rm': [{
                    'command': < CommandModel 1 > ,
                    'strategy': < StrategyCommandModel 15 > ,
                    'test': 'rm'
                }, {
                    'command': < CommandModel 2 > ,
                    'strategy': < StrategyCommandModel 16 > ,
                    'test': 'rm'
                }],
                'cp': [{
                    'command': < CommandModel 3 > ,
                    'strategy': < StrategyCommandModel 15 > ,
                    'test': 'cp'
                }, {
                    'command': < CommandModel 4 > ,
                    'strategy': < StrategyCommandModel 16 > ,
                    'test': 'cp'
                }, {
                    'command': < CommandModel 3 > ,
                    'strategy': < StrategyCommandModel 16 > ,
                    'test': 'cp'
                }]
            }
        """
        data = {}
        for key, value in all_command.items():
            command_info_list = []
            for _value in value:
                command_info_list.append({
                    "block_type": _value.get("command").block_type,
                    "block_info": _value.get("command").block_info,
                    "login_time_limit": eval(_value.get("strategy").login_time_limit),
                    "start_time": _value.get("strategy").start_time,
                    "end_time": _value.get("strategy").end_time
                })
            data[key] = command_info_list
        return data

    def get_command_strategy(self, credential):
        """
        获取凭证以及凭证所在凭证组所有的命令策略
        """
        credential_group_rel_query_set = CredentialGroupRelationshipModel.fetch_all(credential=credential)
        credential_group_query_set = [credential_group_rel_query.credential_group
                                for credential_group_rel_query in credential_group_rel_query_set]
        credential_access_strategy = CredentialGroupStrategyCommandRelationshipModel.fetch_all(credential=credential)
        credential_group_access_strategy = CredentialGroupStrategyCommandRelationshipModel.fetch_all(
                credential_group__in=credential_group_query_set
        )
        command_strategy = []
        for _credential_access_strategy in credential_access_strategy:
            if _credential_access_strategy.strategy_command not in command_strategy:
                command_strategy.append(_credential_access_strategy.strategy_command)
        for _credential_group_access_strategy in credential_group_access_strategy:
            if _credential_group_access_strategy.strategy_command not in command_strategy:
                command_strategy.append(_credential_group_access_strategy.strategy_command)
        return command_strategy

    def get_command_strategy_v2(self, credential_host_query):
        """
        获取凭证以及凭证所在凭证组所有的命令策略
        """
        if credential_host_query.credential_group:
            # 查询绑定改组的
            credential_group = credential_host_query.credential_group
            command_strategy_rel = credential_group.new_credential_group_strategy_command.get_queryset()
        else:
            command_strategy_rel = credential_host_query.new_credential_strategy_command.get_queryset()
        command_strategy = [_command_strategy_rel.strategy_command for _command_strategy_rel in command_strategy_rel]
        return command_strategy


class LinkCheckComponent(CheckUserHostComponent):
    def get_cache(self):
        return get_redis_connection("cache")

    def link_check(self, request):
        """
        {
            "host_id": xx,
            "credential_id": xx,
            "password": "",
            "width": "",
            "height": "",
            "font_size": ""
        }
        """
        data = json.loads(request.body)
        form = LinkCheckForm(data)
        if form.is_valid():
            status, user = self.get_user(request=request)
            if not status:
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有发现有效用户，请联系管理员"))
            credential = CredentialModel.fetch_one(id=form.cleaned_data["credential_id"])
            ip = self.get_access_ip(request)
            status, message, check_data = self.check_user_strategy_access(user, credential, ip)
            if status:
                data.update(**check_data)
                data["host_info"] = HostModel.fetch_one(id=form.cleaned_data.get("host_id")).to_base_dict()
                data["user_id"] = user.id
                token = str(uuid.uuid4())
                self.get_cache().set(token, data)
                response = JsonResponse(success(SuccessStatusCode.OPERATION_SUCCESS, token))
                response.cookies["link_token"] = token
                return response
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="您的操作没有通过访问策略验证"))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=first_error_message(form)))

    def _get_token_info(self, token):
        try:
            data = self.get_cache().get(token).decode("utf-8")
            data = eval(data)
            return True, data
        except Exception as e:
            app_logging.error("[ERROR] LinkCheckComponent, _get_token_info error: {}, param: {}".format(
                    str(e), str(token))
            )
            return False, {}

    def get_token_file_admin(self, token_data):
        if token_data.get("admin"):
            data = {
                "file_download": True,
                "file_upload": True,
                "file_manager": True,
                "copy_tool": True
            }
        else:
            data = {
                "file_download": token_data.get("file_download", False),
                "file_upload": token_data.get("file_upload", False),
                "file_manager": token_data.get("file_manager", False),
                "copy_tool": token_data.get("copy_tool", False)
            }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, data))

    def get_token_host_info(self, token_data):
        data = token_data.get("host_info", {})
        if data.get("ip"):          # 特殊处理外平台连接
            data["host_address"] = data.get("ip")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, data))

    def get_token_info(self, request):
        data = request.GET.dict()
        token = data.get("token")
        status, token_data = self._get_token_info(token)
        if status:
            if data.get("data_type", "") == "host":
                # 获取主机
                return self.get_token_host_info(token_data)
            if data.get("data_type", "") == "file_admin":
                # 获取文件管理
                return self.get_token_file_admin(token_data)
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有发现有效数据"))

    def link_check_v2(self, request):
        data = json.loads(request.body)
        form = LinkCheckV2Form(data)
        if form.is_valid():
            status, user = self.get_user(request=request)
            if not status:
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有发现有效用户，请联系管理员"))
            credential_host = HostCredentialRelationshipModel.fetch_one(id=form.cleaned_data["credential_host_id"])
            ip = self.get_access_ip(request)
            status, message, check_data = self.check_user_strategy_access_v2(user, credential_host, ip)
            if status:
                data.update(**check_data)
                data["host_info"] = HostModel.fetch_one(id=form.cleaned_data.get("host_id")).to_base_dict()
                data["user_id"] = user.id
                token = str(uuid.uuid4())
                self.get_cache().set(token, data)
                response = JsonResponse(success(SuccessStatusCode.OPERATION_SUCCESS, token))
                response.cookies["link_token"] = token
                return response
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="您的操作没有通过访问策略验证"))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=first_error_message(form)))

    def get_cache_token(self, request):
        data = json.loads(request.body)
        token = request.COOKIES.get("bk_token")
        form = GetCacheTokenForm(data)
        esb_obj = EsbApi(token)
        self.create_or_update_current_user(esb_obj)
        self.update_all_import_user_group_info(esb_obj)
        if form.is_valid():
            user = GetUserInfo().get_user_info(bk_token=token)
            cache_token = str(uuid.uuid4())
            cache_token_data = {
                "cache": True,
                "user_id": user.id,
                "host_id": "cache-{}".format(cache_token),
                "host_info": {
                    "ip": form.cleaned_data.get("ip"),
                    "host_name": form.cleaned_data.get("name"),
                    "system_type": form.cleaned_data.get("system_type"),
                    "port": form.cleaned_data.get("ssh_port")
                },
                "file_download": True,
                "file_upload": True,
                "file_manager": True,
                "copy_tool": True
            }
            if form.cleaned_data.get("password") and not form.cleaned_data.get("ssh_key_id"):
                cache_token_data["host_info"]["password"] = form.cleaned_data.get("password")
                cache_token_data["host_info"]["username"] = form.cleaned_data.get("username")
                cache_token_data["login_type"] = "password"
            if form.cleaned_data.get("ssh_key_id"):
                esb_obj = EsbApi(token)
                res = esb_obj.get_user_ssh_key(str(form.cleaned_data.get("ssh_key_id")))
                cache_token_data["login_type"] = "ssh_key"
                if res:
                    cache_token_data["host_info"]["ssh_key"] = res.get("private_key")
                    cache_token_data["host_info"]["password"] = form.cleaned_data.get("password")
                else:
                    return JsonResponse(error(ErrorStatusCode.INPUT_ERROR,
                                              custom_message="无法获取到您选择的秘钥信息，请检查您的数据或联系管理员")
                                        )
            self.get_cache().set(cache_token, cache_token_data)
            response = JsonResponse(success(SuccessStatusCode.OPERATION_SUCCESS, cache_token))
            response.cookies["cache_token"] = cache_token
            return response
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=first_error_message(form)))

    def create_or_update_current_user(self, esb_obj):
        data = esb_obj.get_user_info()
        username = data.pop("username", "")
        current_user = UserInfo.fetch_one(username=username)
        if current_user:
            current_user.update(**{
                "phone": data.get("phone"),
                "email": data.get("email"),
                "ch_name": data.get("ch_name"),
                "role": data.get("role")
            })
        else:
            UserInfo.create(**{
                "username": username,
                "phone": data.get("phone"),
                "email": data.get("email"),
                "ch_name": data.get("ch_name"),
                "role": data.get("role")
            })

    def update_all_import_user_group_info(self, esb_obj):
        res = esb_obj.get_user_group_sync()
        user_query_set = UserInfo.fetch_all()
        # 更新用户信息
        user_list = res.get("user_list")
        group_list = res.get("group_list")
        username_list = [user.get("username") for user in user_list]
        for user_query in user_query_set:
            # 处理已经从RBAC中删除的用户
            if user_query.username not in username_list:
                user_query.delete()
            # 更新已有用户的用户信息
            for user in user_list:
                if user_query.username == user.get("username"):
                    user_query.update(**{
                        "phone": user.get("phone"),
                        "email": user.get("email"),
                        "ch_name": user.get("ch_name"),
                        "role": user.get("role")
                    })
            # 更新用户所在组关系
            current_user_rel = UserGroupRelationshipModel.fetch_all(user=user_query)
            user_group_rel_id = []
            for group in group_list:
                for group_user in group.get("user_list", []):
                    if group_user.get("username") == user_query.username:
                        group_query, _ = UserGroupModel.objects.update_or_create(
                            rbac_group_id=group.get("id"),
                            defaults={"name": group.get("group_name"), "description": group.get("description")}
                        )
                        rel, _ = UserGroupRelationshipModel.objects.update_or_create(
                            user=user_query,
                            user_group=group_query
                        )
                        user_group_rel_id.append(rel.id)
            # 删除无用的关系
            for user_group_rel in current_user_rel:
                if user_group_rel.id not in user_group_rel_id:
                    user_group_rel.delete()
        # 删除已删除的用户组
        group_query_set = UserGroupModel.fetch_all()
        for group_query in group_query_set:
            delete_flag = True
            for group in group_list:
                if group.get("id") == group_query.rbac_group_id:
                    delete_flag = False
            if delete_flag:
                group_query.delete()
        # 删除无关联的用户组
        # for group_query in group_query_set:
        #     if not group_query.group_user.get_queryset():
        #         group_query.delete()


class HostFileComponent(LinkCheckComponent):
    def get_file_info(self, filepath):
        info = {}
        info['TimeModified'] = datetime.datetime.fromtimestamp(os.path.getatime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
        info['Size'] = os.path.getsize(filepath)
        info['Name'] = os.path.basename(filepath)
        return info

    def client_ssh_by_password(self, ip, port, username, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ip, port=port, username=username, password=password, timeout=3)
            return True, ssh
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, client_ssh_by_password error: {}, param: {}".format(
                    str(e), str([ip, port, username, password])
            ))
            return False, None

    def client_ssh_by_ssh_key(self, ip, port, ssh_key, passphrase):
        """
        创建秘钥登陆SSH连接
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            io_pri_key = io.StringIO(ssh_key)
            pri_key = paramiko.RSAKey.from_private_key(io_pri_key, password=passphrase)
            ssh.connect(hostname=ip, port=port, pkey=pri_key, timeout=3)
            return True, ssh
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, client_ssh_by_ssh_key error: {}, param: {}".format(
                    str(e), str([ip, port, ssh_key, passphrase])
            ))
            return False, None

    def get_password(self, password):
        """
        密码解密
        """
        try:
            password = PasswordEncryption().decrypt(password)
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, get_password error: {}, param: {}".format(
                    str(e), str(password)
            ))
            password = ""
        return password

    def _create_ssh_link(self, credential, host, password):
        """
        创建SSH连接
        """
        if credential.login_type == CredentialModel.LOGIN_AUTO:
            if credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                password = self.get_password(credential.login_password)
                login_name = credential.login_name
                status, ssh = self.client_ssh_by_password(host.host_address, host.port, login_name, password)
            else:
                password = credential.passphrase
                ssh_key = credential.ssh_key
                status, ssh = self.client_ssh_by_ssh_key(host.host_address, host.port, ssh_key, password)
        else:
            if credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                login_name = credential.login_name
                status, ssh = self.client_ssh_by_password(host.host_address, host.port, login_name, password)
            else:
                ssh_key = credential.ssh_key
                status, ssh = self.client_ssh_by_ssh_key(host.host_address, host.port, ssh_key, password)
        return status, ssh

    def _create_cache_ssh_link(self, token_data):
        """
        创建SSH连接
        """
        host_info = token_data.get("host_info")
        if token_data.get("login_type") == "password":
            status, ssh = self.client_ssh_by_password(
                    host_info.get("ip"),
                    host_info.get("port"),
                    host_info.get("username"),
                    host_info.get("password")
            )
        else:
            status, ssh = self.client_ssh_by_ssh_key(
                    host_info.get("ip"),
                    host_info.get("port"),
                    host_info.get("ssh_key"),
                    host_info.get("password")
            )
        return status, ssh

    def get_sftp(self, token_data):
        if not token_data.get("cache"):
            host_id = token_data.get("host_id")
            credential_host_id = token_data.get("credential_host_id")
            password = token_data.get("password")
            credential_host = HostCredentialRelationshipModel.fetch_one(id=credential_host_id)
            host = HostModel.fetch_one(id=host_id)
            status, ssh = self._create_ssh_link(credential_host.credential, host, password)
            if status:
                stdin, stdout, stderr = ssh.exec_command('pwd')
                home_path = stdout.read().decode().strip('\n')
                sftp = ssh.open_sftp()
                return True, "", {"ssh": ssh, "sftp": sftp, "home_path": home_path}
            return False, "连接主机失败", {}
        else:
            status, ssh = self._create_cache_ssh_link(token_data)
            if status:
                stdin, stdout, stderr = ssh.exec_command('pwd')
                home_path = stdout.read().decode().strip('\n')
                sftp = ssh.open_sftp()
                return True, "", {"ssh": ssh, "sftp": sftp, "home_path": home_path}
            return False, "连接主机失败", {}

    def get_linux_file_list(self, data, token_data):
        status, message, sftp_data = self.get_sftp(token_data)
        if status:
            ssh = sftp_data.get("ssh")
            sftp = sftp_data.get("sftp")
            home_path = sftp_data.get("home_path")
            url = data.get("url")
            if url:
                path = '/' + url.strip('/')
            else:
                path = home_path
            if re.search('\.\./', path):
                return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
            data = {
                    "current_path": path
                }
            folder_list = {"path": [], "file": []}
            sftp.chdir(path)
            for r in sftp.listdir_attr():
                if r.filename.startswith("."):
                    continue
                if r.longname.startswith('d'):
                    folder_list["path"].append(r.filename)
                else:
                    folder_list["file"].append(r.filename)
            data['data'] = folder_list
            ssh.close()
            return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, data))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))

    def download_linux_file(self, data, token_data):
        status, message, sftp_data = self.get_sftp(token_data)
        if status:
            tmp_dir = '/tmp/terminal_file/'
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)
            url = data.get("url")
            ssh = sftp_data.get("ssh")
            sftp = sftp_data.get("sftp")
            home_path = sftp_data.get("home_path")
            if url:
                path = '/' + url.strip('/')
            else:
                path = home_path
            if re.search('\.\./', path):
                return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
            filename = path.split('/').pop()
            full_path = tmp_dir + filename
            sftp.get(path, full_path)
            ssh.close()
            with open(full_path, 'rb') as f:
                c = f.read()
            response = HttpResponse(c)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=' + os.path.basename(full_path)
            return response
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))

    def get_linux_file(self, request):
        data = request.GET.dict()
        token = data.get("token")
        status, token_data = self._get_token_info(token)
        if status:
            # 判定操作类型
            data_type = data.get("data_type")
            if data_type == "file_list":
                if token_data.get("file_manager") or token_data.get("admin"):
                    return self.get_linux_file_list(data, token_data)
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="当前凭证没有文件管理权限"))
            if data_type == "file":
                if token_data.get("file_download") or token_data.get("admin"):
                    return self.download_linux_file(data, token_data)
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="当前凭证没有下载文件权限"))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有发现有效数据"))

    def upload_linux_file(self, request):
        kwargs = request.POST
        file_obj = request.FILES.get('file', None)
        token = kwargs.get('token')
        status, token_data = self._get_token_info(token)
        if status:
            if not token_data.get("file_upload") and not token_data.get("admin"):
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="当前凭证没有文件上传权限"))
            try:
                status, message, sftp_data = self.get_sftp(token_data)
                if status:
                    ssh = sftp_data.get("ssh")
                    sftp = sftp_data.get("sftp")
                    home_path = sftp_data.get("home_path")
                    if kwargs.get("url"):
                        path = '/' + kwargs.get("url").strip('/')
                    else:
                        path = home_path
                    if re.search('\.\./', path):
                        return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
                    if not sftp:
                        return JsonResponse(error(ErrorStatusCode.LINK_LINUX_ERROR))
                    tmp_dir = '/tmp/terminal_file/'
                    if not os.path.exists(tmp_dir):
                        os.makedirs(tmp_dir)
                    full_path = tmp_dir + file_obj.name
                    with open(full_path, 'wb') as f:
                        for line in file_obj.chunks():
                            f.write(line)
                    f.close()
                    sftp.put(full_path, os.path.join(path, file_obj.name))
                    ssh.close()
                    return JsonResponse(success(SuccessStatusCode.UPLOAD_SUCCESS))
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
            except Exception as e:
                app_logging.error("[ERROR] Upload linux file error, error: {}, param: {}".format(str(e), token))
                return JsonResponse(error(ErrorStatusCode.UPLOAD_ERROR))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有发现有效数据"))

    def delete_linux_file(self, request):
        data = json.loads(request.body)
        token = data.get("token")
        status, token_data = self._get_token_info(token)
        if status:
            if not token_data.get("file_manager") and not token_data.get("admin"):
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="当前凭证没有文件管理权限"))
            status, message, sftp_data = self.get_sftp(token_data)
            if status:
                ssh = sftp_data.get("ssh")
                sftp = sftp_data.get("sftp")
                home_path = sftp_data.get("home_path")
                if data.get("url"):
                    path = '/' + data.get("url").strip('/')
                else:
                    path = '/root'
                if re.search('\.\./', path):
                    return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
                try:
                    if not path:
                        path = home_path
                    if path == home_path:
                        return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
                    sftp.remove(path)
                except OSError:
                    sftp.rmdir(path)
                    return JsonResponse(error(ErrorStatusCode.DELETE_ERROR))
                except Exception as e:
                    return JsonResponse(error(ErrorStatusCode.HANDLE_ERROR))
                finally:
                    ssh.close()
                return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有发现有效数据"))

    def get_windows_file_list(self, data, token_data):
        base_path = '/' + settings.ORI_GUACD_PATH.strip('/') + '/' + str(token_data.get("host_id"))
        if not os.path.exists(base_path + "/Download"):
            os.makedirs(base_path + "/Download")
        if data.get("url"):
            path = data.get("url").strip('/')
        else:
            path = "Download"
        if re.search('\.\./', path):
            return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
        data = {
            'current_path': path
        }
        full_path = os.path.join(base_path, path)
        if not os.path.exists(full_path):
            return JsonResponse(error(ErrorStatusCode.DATA_NOT_EXISTED))
        try:
            ps = os.listdir(full_path)
            folder_list = {"path": [], "file": []}
            for n in ps:
                v = os.path.join(full_path, n)
                if os.path.isdir(v):
                    folder_list["path"].append(n)
                else:
                    folder_list["file"].append(n)
            data['data'] = folder_list
            return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, data))
        except Exception as e:
            return JsonResponse(error(ErrorStatusCode.CUSTOM_ERROR, custom_message=str(e)))

    def download_windows_file(self, data, token_data):
        base_path = '/' + settings.ORI_GUACD_PATH.strip('/') + '/' + str(token_data.get("host_id"))
        if not os.path.exists(base_path + "/Download"):
            os.makedirs(base_path + "/Download")
        if data.get("url"):
            path = data.get("url").strip('/')
        else:
            path = "Download"
        if re.search('\.\./', path):
            return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
        full_path = os.path.join(base_path, path)
        if not os.path.exists(full_path):
            return JsonResponse(error(ErrorStatusCode.DATA_NOT_EXISTED))
        try:
            with open(full_path, 'rb') as f:
                c = f.read()
            response = HttpResponse(c)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=' + os.path.basename(full_path)
            return response
        except Exception as e:
            return JsonResponse(error(ErrorStatusCode.CUSTOM_ERROR, custom_message=str(e)))

    def get_windows_file(self, request):
        data = request.GET.dict()
        token = data.get("token")
        status, token_data = self._get_token_info(token)
        if status:
            # 判定操作类型
            data_type = data.get("data_type")
            if data_type == "file_list":
                if token_data.get("file_manager") or token_data.get("admin"):
                    return self.get_windows_file_list(data, token_data)
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="当前凭证没有文件管理权限"))
            if data_type == "file":
                if token_data.get("file_download") or token_data.get("admin"):
                    return self.download_windows_file(data, token_data)
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="当前凭证没有下载文件权限"))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有发现有效数据"))

    def upload_windows_file(self, request):
        kwargs = request.POST
        file_obj = request.FILES.get('file', None)
        token = kwargs.get('token')
        status, token_data = self._get_token_info(token)
        if status:
            if not token_data.get("file_upload") and not token_data.get("admin"):
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="当前凭证没有文件上传权限"))
            if not kwargs.get("url"):
                path = "Download"
            else:
                path = kwargs.get("url").strip('/')
            if re.search('\.\./', path):
                return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
            base_path = '/' + settings.ORI_GUACD_PATH.strip('/') + '/' + str(token_data.get("host_id"))
            full_path = os.path.join(base_path, path)
            if not os.path.exists(full_path):
                return JsonResponse(error(ErrorStatusCode.DATA_NOT_EXISTED))
            with open(os.path.join(full_path, file_obj.name), 'wb') as f:
                for line in file_obj.chunks():
                    f.write(line)
            f.close()
            return JsonResponse(success(SuccessStatusCode.UPLOAD_SUCCESS))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有发现有效数据"))

    def delete_windows_file(self, request):
        data = json.loads(request.body)
        token = data.get("token")
        status, token_data = self._get_token_info(token)
        if status:
            if not token_data.get("file_manager") and not token_data.get("admin"):
                return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="当前凭证没有文件管理权限"))
            if not data.get("url"):
                path = "Download"
            else:
                path = data.get("url").strip('/')
            if re.search('\.\./', path) or path == "Download":
                return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
            base_path = '/' + settings.ORI_GUACD_PATH.strip('/') + '/' + str(token_data.get("host_id"))
            full_path = os.path.join(base_path, path)
            if os.path.exists(full_path):
                if os.path.isdir(full_path):
                    os.rmdir(full_path)
                else:
                    os.remove(full_path)
            else:
                return JsonResponse(error(ErrorStatusCode.DATA_NOT_EXISTED))
            return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有发现有效数据"))

# if __name__ == '__main__':
#     import os
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
#     import sys
#     os.environ["BK_ENV"] = os.getenv("BK_ENV", "development")
#     # os.environ.setdefault("BK_ENV", "production")     # 生产环境解注改行
#     # os.environ.setdefault("BK_ENV", "testing")        # 开发环境解注改行
#     sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
#     import django
#     from config import *
#     django.setup()
#     import json
#     from django.http import JsonResponse
#     import uuid
#     from django_redis import get_redis_connection
#     import datetime
#     import logging
#
#     from bastion.forms.core_form import LinkCheckForm
#     from bastion.forms import first_error_message
#     from bastion.models import HostModel, UserInfo, CredentialModel, CredentialGroupRelationshipModel, \
#         StrategyAccessModel, UserGroupRelationshipModel, StrategyAccessUserGroupRelationshipModel, \
#         CredentialGroupStrategyAccessRelationshipModel, StrategyCommandModel, StrategyCommandGroupRelationshipModel, \
#         CredentialGroupStrategyCommandRelationshipModel
#     from bastion.utils.status_code import success, error, SuccessStatusCode, ErrorStatusCode
#     from bastion.component.common import GetUserInfo
#
#     # app_logging = logging.getLogger("app")
#     # CheckUserHostComponent().handle_command_strategy([])
#     a = StrategyCommandModel.fetch_all()
#     # CheckUserHostComponent().handle_command_strategy(a)
#     # command = "ls && ls && cat /etc/hosts || reboot"
#     # command = "ls | grep rm && cp&&rm | mkdir && tar;ls"
#     # command = "ls && ls && cat /etc/hosts || rm"
#     command = "ls&& rm; rm|grep rm&& cp"
#     # res = CheckUserHostComponent().check_command("test", command)
#     user = UserInfo.fetch_one(username="guoyuchen")
#     credential = CredentialModel.fetch_one(id=37)
#     status, message, res = CheckUserHostComponent().check_user_strategy_access(user, credential, "127.0.0.1")
#     print(res.get("command_data"))
#     _res = CheckUserHostComponent().check_access_strategy(res.get("access_data"), "127.0.0.1")
#     _res = CheckUserHostComponent().check_command(res.get("command_data"), "rm")
#     print(_res)


