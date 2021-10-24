import json
from django.http import JsonResponse
import logging

from bastion.models import StrategyAccessModel, StrategyAccessUserGroupRelationshipModel, \
    CredentialGroupStrategyAccessRelationshipModel, StrategyCommandModel, StrategyCommandGroupRelationshipModel, \
    StrategyCommandUserGroupRelationshipModel, CredentialGroupStrategyCommandRelationshipModel, \
    HostCredentialRelationshipModel, CredentialModel, CredentialGroupModel, HostModel
from bastion.forms.strategy_from import AccessStrategyForm, CommandStrategyForm
from bastion.forms import first_error_message
from bastion.utils.status_code import success, error, SuccessStatusCode, ErrorStatusCode
from bastion.component.common import GetUserInfo

app_logging = logging.getLogger("app")


class BaseComponent:
    def check_unique(self, model, args):
        query = model.fetch_one(**args)
        if query:
            return True, "记录已存在", query
        return False, "没有找到相关信息", None

    def update_strategy_status(self, request):
        data = json.loads(request.body)
        if data.get("type", "") == "command":
            model = StrategyCommandModel
        elif data.get("type", "") == "access":
            model = StrategyAccessModel
        else:
            model = None
        if model:
            status, message, query = self.check_unique(model, {"id": data.get("id")})
            if status:
                strategy_status = data.get("status", True)
                try:
                    new_qeury = query.update(**{"status": strategy_status})
                except Exception as e:
                    app_logging.error("[ERROR] Update strategy status error: {}, param: {}".format(
                        str(e), str(data)
                    ))
                    new_qeury = query.update(**{"status": False})
                return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, new_qeury.to_all_dict()))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="您输入的参数有误"))

    def get_group_resource_credential(self, data):
        group = CredentialGroupModel.fetch_all()
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, [
            _group.to_base_dict() for _group in group
        ]))

    def get_password_resource_credential(self, data):
        resource_credential = HostCredentialRelationshipModel.fetch_all(
            credential__credential_type=CredentialModel.CREDENTIAL_PASSWORD,
            credential_group=None
        )
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, [
            _resource_credential.to_base_dict() for _resource_credential in resource_credential
        ]))

    def get_ssh_resource_credential(self, data):
        resource_credential = HostCredentialRelationshipModel.fetch_all(
            credential__credential_type=CredentialModel.CREDENTIAL_SSH_KEY,
            credential_group=None
        )
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, [
            _resource_credential.to_base_dict() for _resource_credential in resource_credential
        ]))

    def get_host_resource_credential(self, data):
        host_id = int(data.get("host_id"))
        user_query = data.get("user")
        if not user_query:
            return False, "用户不存在"
        status, message, query = self.check_unique(HostModel, {"id": host_id})
        if status:
            if user_query.role == 1:
                resource_credential = HostCredentialRelationshipModel.fetch_all(host=query)
            else:
                host_credential_queryset = user_query.get_host_credential_queryset()
                resource_credential = [host_credential_query for host_credential_query in host_credential_queryset if host_credential_query.host==query]
            return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, [
                _resource_credential.to_base_dict() for _resource_credential in resource_credential
            ]))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))

    def get_resource_credential(self, request):
        data = request.GET.dict()
        data_type = data.get("data_type")
        if data_type == "ssh":
            return self.get_ssh_resource_credential(data)
        if data_type == "password":
            return self.get_password_resource_credential(data)
        if data_type == "group":
            return self.get_group_resource_credential(data)
        if data_type == "host":
            data["user"] = GetUserInfo().get_user_info(request)
            return self.get_host_resource_credential(data)
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR))


class AccessStrategyComponent(BaseComponent):
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

    def _create_access_strategy_credential(self, form, strategy_query):
        credential_info = form.cleaned_data["credential"]
        password_credential = credential_info.get("password_credential", [])
        ssh_credential = credential_info.get("ssh_credential", [])
        credential_group = credential_info.get("credential_group", [])
        try:
            if password_credential:
                for _credential in password_credential:
                    CredentialGroupStrategyAccessRelationshipModel.objects.get_or_create(**{
                        "strategy_access": strategy_query,
                        "credential_id": _credential
                    })
            if ssh_credential:
                for _credential in ssh_credential:
                    CredentialGroupStrategyAccessRelationshipModel.objects.get_or_create(**{
                        "strategy_access": strategy_query,
                        "credential_id": _credential
                    })
            if credential_group:
                for _credential_group in credential_group:
                    CredentialGroupStrategyAccessRelationshipModel.objects.get_or_create(**{
                        "strategy_access": strategy_query,
                        "credential_group_id": _credential_group
                    })
            return True
        except Exception as e:
            error_info = "[ERROR] Create access strategy user error: {}, param: {}".format(str(e), str(credential_info))
            app_logging.error(error_info)
            # print(error_info)
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
                "user_group": [1]               # 用户组id             与用户不共存
            },
            "credential": {                             # 三者不共存
                "password_credential": [1, 2],
                "ssh_credential": [1, 2],
                "credential_group": [1, 2],
            }
        }
        """
        data = json.loads(request.body)
        form = AccessStrategyForm(data)
        if form.is_valid():
            status, message, query = self.check_unique(StrategyAccessModel, {
                "name": form.cleaned_data["strategy"].get("name")
            })
            if not status:
                create_user = GetUserInfo().get_user_info(request)
                create_access_strategy_status, query = self._create_or_update_access_strategy(form, create_user)
                create_access_strategy_user_status = self._create_access_strategy_user(form, query)
                create_access_strategy_credential_status = self._create_access_strategy_credential(form, query)
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
        credential_relationships = query.strategy_access_credential_or_credential_group.get_queryset()
        for credential_relationship in credential_relationships:
            credential_relationship.delete()

    def update_access_strategy(self, request):
        data = json.loads(request.body)
        form = AccessStrategyForm(data)
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
                    create_access_strategy_credential_status = self._create_access_strategy_credential(form, query)
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


class CommandStrategyComponent(BaseComponent):
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

    def _create_command_strategy_credential(self, form, strategy_query):
        credential_info = form.cleaned_data["credential"]
        password_credential = credential_info.get("password_credential", [])
        ssh_credential = credential_info.get("ssh_credential", [])
        credential_group = credential_info.get("credential_group", [])
        try:
            if password_credential:
                for _credential in password_credential:
                    CredentialGroupStrategyCommandRelationshipModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "credential_id": _credential
                    })
            if ssh_credential:
                for _credential in ssh_credential:
                    CredentialGroupStrategyCommandRelationshipModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "credential_id": _credential
                    })
            if credential_group:
                for _credential_group in credential_group:
                    CredentialGroupStrategyCommandRelationshipModel.objects.get_or_create(**{
                        "strategy_command": strategy_query,
                        "credential_group_id": _credential_group
                    })
            return True
        except Exception as e:
            error_info = "[ERROR] Create access strategy user error: {}, param: {}".format(str(e), str(credential_info))
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
            "credential": {                             # 三者不共存
                "password_credential": [1, 2],
                "ssh_credential": [1, 2],
                "credential_group": [1, 2],
            }
        }
        """
        data = json.loads(request.body)
        form = CommandStrategyForm(data)
        if form.is_valid():
            status, message, query = self.check_unique(StrategyCommandModel, {
                "name": form.cleaned_data["strategy"].get("name")
            })
            if not status:
                create_user = GetUserInfo().get_user_info(request)
                create_command_strategy_status, query = self._create_or_update_command_strategy(form, create_user)
                create_command_strategy_command_status = self._create_command_strategy_command(form, query)
                create_command_strategy_user_status = self._create_command_strategy_user(form, query)
                create_command_strategy_credential_status = self._create_command_strategy_credential(form, query)
                if create_command_strategy_status and create_command_strategy_user_status \
                        and create_command_strategy_credential_status and create_command_strategy_command_status:
                    return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, query.to_all_dict()))
                return JsonResponse(error(ErrorStatusCode.SERVER_ERROR))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="策略名称已存在"))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=first_error_message(form)))

    def _clean_relationship(self, query: StrategyCommandModel):
        user_relationships = query.strategy_command_user_or_user_group.get_queryset()
        for user_relationship in user_relationships:
            user_relationship.delete()
        credential_relationships = query.strategy_command_credential_or_credential_group.get_queryset()
        for credential_relationship in credential_relationships:
            credential_relationship.delete()
        command_relationships = query.strategy_command_or_group.get_queryset()
        for command_relationship in command_relationships:
            command_relationship.delete()

    def update_command_strategy(self, request):
        data = json.loads(request.body)
        form = CommandStrategyForm(data)
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
                    create_access_strategy_credential_status = self._create_command_strategy_credential(form, query)
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
