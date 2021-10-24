import json
from django.http import JsonResponse
import logging

from bastion.models import StrategyAccessModel, StrategyAccessUserGroupRelationshipModel, \
    StrategyAccessCredentialHostModel, StrategyCommandModel, StrategyCommandGroupRelationshipModel, \
    StrategyCommandUserGroupRelationshipModel, StrategyCommandCredentialHostModel
from bastion.component.strategy import BaseComponent
from bastion.forms.strategy_v2_form import AccessStrategyV2Form, CommandStrategyV2Form
from bastion.utils.status_code import success, error, SuccessStatusCode, ErrorStatusCode
from bastion.component.common import GetUserInfo
from bastion.forms import first_error_message

app_logging = logging.getLogger("app")


class AccessStrategyV2Component(BaseComponent):
    def _get_one_access_strategy(self, data):
        status, message, query = self.check_unique(StrategyAccessModel, {"id": data.get("id")})
        if status:
            return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, query.to_all_dict()))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))

    def _page_access_strategy(self, data):
        page = int(data.get("current", 1))
        per_page = int(data.get("pageSize", 10))
        search_type = data.get("search_type", "")
        search_data = data.get("search_data", None)
        filter_dict = {}
        if search_data and search_type:
            filter_dict[search_type + "__contains"] = search_data
        query_set, total = StrategyAccessModel.pagination(page, per_page, **filter_dict)
        end_data = {
            "current": page,
            "pageSize": per_page,
            "total": total,
            "data": [query.to_list_dict() for query in query_set]
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))

    def get_access_strategy(self, request):
        data = request.GET.dict()
        if data.get("id"):
            return self._get_one_access_strategy(data)
        else:
            return self._page_access_strategy(data)

    def _create_or_update_access_strategy(self, form, create_user=None, query=None):
        strategy_info = form.cleaned_data["strategy"]
        create_dict = {
                "name": strategy_info.get("name"),
                "start_time": strategy_info.get("start_time") if strategy_info.get("start_time") else None,
                "end_time": strategy_info.get("end_time") if strategy_info.get("end_time") else None,
                "file_upload": strategy_info.get("file_upload", False),
                "file_download": strategy_info.get("file_download", False),
                "file_manager": strategy_info.get("file_manager", False),
                "copy_tool": strategy_info.get("copy_tool", False),
                "login_time_limit": strategy_info.get("login_time_limit"),
                "ip_limit": strategy_info.get("ip_limit"),
                "limit_list": strategy_info.get("limit_list") if strategy_info.get("limit_list") else [],
                "user": create_user,
            }
        if create_user:
            try:
                access_srategy_object = StrategyAccessModel.create(**create_dict)
                return True, access_srategy_object
            except Exception as e:
                error_info = "[ERROR] Create access strategy error: {}, param: {}".format(str(e), str(create_dict))
                app_logging.error(error_info)
                # print(error_info)
                return False, None
        else:
            try:
                create_dict.pop("name", "")
                access_srategy_object = query.update(**create_dict)
                return True, access_srategy_object
            except Exception as e:
                error_info = "[ERROR] Update access strategy error: {}, param: {}".format(str(e), str(create_dict))
                app_logging.error(error_info)
                # print(error_info)
                return False, None

    def _create_access_strategy_user(self, form, strategy_query):
        user_info = form.cleaned_data["user"]
        user = user_info.get("user", [])
        user_group = user_info.get("user_group", [])
        try:
            if user:
                for _user in user:
                    StrategyAccessUserGroupRelationshipModel.objects.get_or_create(**{
                        "strategy_access": strategy_query,
                        "user_id": _user
                    })
            if user_group:
                for _user_group in user_group:
                    StrategyAccessUserGroupRelationshipModel.objects.get_or_create(**{
                        "strategy_access": strategy_query,
                        "user_group_id": _user_group
                    })
            return True
        except Exception as e:
            error_info = "[ERROR] Create access strategy user error: {}, param: {}".format(str(e), str(user_info))
            app_logging.error(error_info)
            # print(error_info)
            return False

    def _create_access_strategy_credential_host(self, form, strategy_query):
        credential_host = form.cleaned_data["credential_host"]
        password_credential_host_id = credential_host.get("password_credential_host_id", [])
        ssh_credential_host_id = credential_host.get("ssh_credential_host_id", [])
        credential_group = credential_host.get("credential_group", [])
        try:
            if password_credential_host_id:
                for _password_credential_host_id in password_credential_host_id:
                    StrategyAccessCredentialHostModel.objects.get_or_create(**{
                        "strategy_access": strategy_query,
                        "credential_host_id": _password_credential_host_id
                    })
            if ssh_credential_host_id:
                for _ssh_credential_host_id in ssh_credential_host_id:
                    StrategyAccessCredentialHostModel.objects.get_or_create(**{
                        "strategy_access": strategy_query,
                        "credential_host_id": _ssh_credential_host_id
                    })
            if credential_group:
                for _credential_group in credential_group:
                    StrategyAccessCredentialHostModel.objects.get_or_create(**{
                        "strategy_access": strategy_query,
                        "credential_group_id": _credential_group
                    })
            return True
        except Exception as e:
            error_info = "[ERROR] Create access strategy user error: {}, param: {}".format(str(e), str(credential_host))
            app_logging.error(error_info)
            return False

    def create_access_strategy(self, request):
        """
        {
            "strategy": {
                "name": "",
                "start_time": "",
                "end_time": "",
                "file_download": "",
                "file_manager": "",
                "copy_tool": "",
                "login_time_limit": [
                    {"week": 1, "time": [1, 2, 3, 4]},
                    {"week": 2, "time": [1, 2, 3, 4]},
                    {"week": 3, "time": [1, 2, 3, 4]},
                ],
                "ip_limit": 1,
                "limit_list": []
            },
            "user": {
                "user": [1, 2]                  # 用户id
                "user_group": [1]               # 用户组id
            },
            "credential_host": {
                "password_credential_host_id": [1, 2],
                "ssh_credential_host_id": [1, 2],       # 这个是资源凭证的ID
                "credential_group": [1, 2]              # 这个是凭证组ID
            }
        }
        """
        data = json.loads(request.body)
        form = AccessStrategyV2Form(data)
        if form.is_valid():
            status, message, query = self.check_unique(StrategyAccessModel, {
                "name": form.cleaned_data["strategy"].get("name")
            })
            if not status:
                create_user = GetUserInfo().get_user_info(request)
                create_access_strategy_status, query = self._create_or_update_access_strategy(form, create_user)
                create_access_strategy_user_status = self._create_access_strategy_user(form, query)
                create_access_strategy_credential_status = self._create_access_strategy_credential_host(form, query)
                if create_access_strategy_credential_status and create_access_strategy_status \
                        and create_access_strategy_user_status:
                    return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, query.to_all_dict()))
                return JsonResponse(error(ErrorStatusCode.SERVER_ERROR))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="策略名称已存在"))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=first_error_message(form)))

    def _clean_relationship(self, query: StrategyAccessModel):
        user_relationships = query.strategy_access_user_or_user_group.get_queryset()
        for user_relationship in user_relationships:
            user_relationship.delete()
        host_credential_relationships = query.new_strategy_access_credential_or_credential_group.get_queryset()
        for host_credential_relationship in host_credential_relationships:
            host_credential_relationship.delete()

    def update_access_strategy(self, request):
        data = json.loads(request.body)
        form = AccessStrategyV2Form(data)
        if form.is_valid():
            status, message, query = self.check_unique(StrategyAccessModel, {
                "id": form.cleaned_data["strategy"].get("id")
            })
            if status:
                update_access_strategy_status, query = self._create_or_update_access_strategy(form, query=query)
                if update_access_strategy_status:
                    # 清除所有关联关系
                    self._clean_relationship(query)
                    create_access_strategy_user_status = self._create_access_strategy_user(form, query)
                    create_access_strategy_credential_status = self._create_access_strategy_credential_host(form, query)
                    if create_access_strategy_credential_status and update_access_strategy_status \
                        and create_access_strategy_user_status:
                        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, query.to_all_dict()))
                return JsonResponse(error(ErrorStatusCode.SERVER_ERROR))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有找到对应的信息"))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=first_error_message(form)))

    def delete_access_strategy(self, request):
        data = json.loads(request.body)
        id = data.get("id")
        status, message, query = self.check_unique(StrategyAccessModel, {"id": id})
        if status:
            query.delete()
            return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))


class CommandStrategyV2Component(BaseComponent):
    def _get_one_command_strategy(self, data):
        status, message, query = self.check_unique(StrategyCommandModel, {"id": data.get("id")})
        if status:
            return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, query.to_all_dict()))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))

    def _page_command_strategy(self, data):
        page = int(data.get("current", 1))
        per_page = int(data.get("pageSize", 10))
        search_type = data.get("search_type", "")
        search_data = data.get("search_data", None)
        filter_dict = {}
        if search_data and search_type:
            filter_dict[search_type + "__contains"] = search_data
        query_set, total = StrategyCommandModel.pagination(page, per_page, **filter_dict)
        end_data = {
            "current": page,
            "pageSize": per_page,
            "total": total,
            "data": [query.to_list_dict() for query in query_set]
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))

    def get_command_strategy(self, request):
        data = request.GET.dict()
        if data.get("id"):
            return self._get_one_command_strategy(data)
        else:
            return self._page_command_strategy(data)

    def _create_or_update_command_strategy(self, form, create_user=None, query=None):
        strategy_info = form.cleaned_data["strategy"]
        create_dict = {
                "name": strategy_info.get("name"),
                "start_time": strategy_info.get("start_time") if strategy_info.get("start_time") else None,
                "end_time": strategy_info.get("end_time") if strategy_info.get("end_time") else None,
                "login_time_limit": strategy_info.get("login_time_limit"),
                "user": create_user,
            }
        if create_user:
            try:
                access_srategy_object = StrategyCommandModel.create(**create_dict)
                return True, access_srategy_object
            except Exception as e:
                error_info = "[ERROR] Create access strategy error: {}, param: {}".format(str(e), str(create_dict))
                app_logging.error(error_info)
                # print(error_info)
                return False, None
        else:
            try:
                create_dict.pop("name", "")
                access_srategy_object = query.update(**create_dict)
                return True, access_srategy_object
            except Exception as e:
                error_info = "[ERROR] Update access strategy error: {}, param: {}".format(str(e), str(create_dict))
                app_logging.error(error_info)
                # print(error_info)
                return False, None

    def _create_command_strategy_command(self, form, strategy_query):
        command_info = form.cleaned_data["command"]
        command = command_info.get("command", [])
        command_group = command_info.get("command_group", [])
        try:
            if command:
                for _command in command:
                    StrategyCommandGroupRelationshipModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "command_id": _command
                    })
            if command_group:
                for _command_group in command_group:
                    StrategyCommandGroupRelationshipModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "command_group_id": _command_group
                    })
            return True
        except Exception as e:
            error_info = "[ERROR] Create access strategy user error: {}, param: {}".format(str(e), str(command_info))
            app_logging.error(error_info)
            # print(error_info)
            return False

    def _create_command_strategy_user(self, form, strategy_query):
        user_info = form.cleaned_data["user"]
        user = user_info.get("user", [])
        user_group = user_info.get("user_group", [])
        try:
            if user:
                for _user in user:
                    StrategyCommandUserGroupRelationshipModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "user_id": _user
                    })
            if user_group:
                for _user_group in user_group:
                    StrategyCommandUserGroupRelationshipModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "user_group_id": _user_group
                    })
            return True
        except Exception as e:
            error_info = "[ERROR] Create access strategy user error: {}, param: {}".format(str(e), str(user_info))
            app_logging.error(error_info)
            # print(error_info)
            return False

    def _create_command_strategy_credential_host(self, form, strategy_query):
        credential_info = form.cleaned_data["credential_host"]
        password_credential_host_id = credential_info.get("password_credential_host_id", [])
        ssh_credential_host_id = credential_info.get("ssh_credential_host_id", [])
        credential_group = credential_info.get("credential_group", [])
        try:
            if password_credential_host_id:
                for _credential_host in password_credential_host_id:
                    StrategyCommandCredentialHostModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "credential_host_id": _credential_host
                    })
            if ssh_credential_host_id:
                for _credential_host in ssh_credential_host_id:
                    StrategyCommandCredentialHostModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "credential_host_id": _credential_host
                    })
            if credential_group:
                for _credential_group in credential_group:
                    StrategyCommandCredentialHostModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "credential_group_id": _credential_group
                    })
            return True
        except Exception as e:
            error_info = "[ERROR] Create access strategy user error: {}, param: {}".format(str(e), str(credential_info))
            app_logging.error(error_info)
            # print(error_info)
            return False

    def _clean_relationship(self, query: StrategyCommandModel):
        user_relationships = query.strategy_command_user_or_user_group.get_queryset()
        for user_relationship in user_relationships:
            user_relationship.delete()
        host_credential_relationships = query.new_strategy_command_credential_or_credential_group.get_queryset()
        for host_credential_relationship in host_credential_relationships:
            host_credential_relationship.delete()
        command_relationships = query.strategy_command_or_group.get_queryset()
        for command_relationship in command_relationships:
            command_relationship.delete()

    def create_command_strategy(self, request):
        """
        {
            "strategy": {
                "name": "",
                "start_time": "",
                "end_time": "",
                "login_time_limit": [
                    {"week": 1, "time": [1, 2, 3, 4]},
                    {"week": 2, "time": [1, 2, 3, 4]},
                    {"week": 3, "time": [1, 2, 3, 4]},
                ]
            },
            "command": {
                "command": [1, 2],
                "command_group": [1, 2]
            },
            "user": {
                "user": [1, 2]                  # 用户id
                "user_group": [1]               # 用户组id             与用户不共存
            },
            "credential_host": {
                "password_credential_host_id": [1, 2],
                "ssh_credential_host_id": [1, 2],
                "credential_group": [1, 2]
            }
        }
        """
        data = json.loads(request.body)
        form = CommandStrategyV2Form(data)
        if form.is_valid():
            status, message, query = self.check_unique(StrategyCommandModel, {
                "name": form.cleaned_data["strategy"].get("name")
            })
            if not status:
                create_user = GetUserInfo().get_user_info(request)
                create_command_strategy_status, query = self._create_or_update_command_strategy(form, create_user)
                create_command_strategy_command_status = self._create_command_strategy_command(form, query)
                create_command_strategy_user_status = self._create_command_strategy_user(form, query)
                create_command_strategy_credential_status = self._create_command_strategy_credential_host(form, query)
                if create_command_strategy_status and create_command_strategy_user_status \
                        and create_command_strategy_credential_status and create_command_strategy_command_status:
                    return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, query.to_all_dict()))
                return JsonResponse(error(ErrorStatusCode.SERVER_ERROR))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="策略名称已存在"))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=first_error_message(form)))

    def update_command_strategy(self, request):
        data = json.loads(request.body)
        form = CommandStrategyV2Form(data)
        if form.is_valid():
            status, message, query = self.check_unique(StrategyCommandModel, {
                "id": form.cleaned_data["strategy"].get("id")
            })
            if status:
                update_access_strategy_status, query = self._create_or_update_command_strategy(form, query=query)
                if update_access_strategy_status:
                    # 清除所有关联关系
                    self._clean_relationship(query)
                    create_access_strategy_user_status = self._create_command_strategy_user(form, query)
                    create_command_strategy_command_status = self._create_command_strategy_command(form, query)
                    create_access_strategy_credential_status = self._create_command_strategy_credential_host(form, query)
                    if create_access_strategy_credential_status and update_access_strategy_status \
                        and create_access_strategy_user_status and create_command_strategy_command_status:
                        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, query.to_all_dict()))
                return JsonResponse(error(ErrorStatusCode.SERVER_ERROR))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="没有找到对应的信息"))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=first_error_message(form)))

    def delete_command_strategy(self, request):
        data = json.loads(request.body)
        id = data.get("id")
        status, message, query = self.check_unique(StrategyCommandModel, {"id": id})
        if status:
            query.delete()
            return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))

