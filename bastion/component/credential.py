import json
import logging

from django.http import JsonResponse

from bastion.component.audit import OperationLog
from bastion.component.common import GetModelData, GetUserInfo

from bastion.forms import first_error_message
from bastion.forms.forms import CredentialGroupModelForm, CredentialModelForm, GroupCredentialModelForm, \
    CommandGroupModelForm, GroupCommandModelForm, CommandModelForm
from bastion.models import CredentialGroupModel, CredentialModel, CredentialGroupRelationshipModel, CommandGroupModel, \
    CommandGroupRelationshipModel, CommandModel, HostModel, HostCredentialRelationshipModel
from bastion.utils.decorator import sync_user_and_group
from bastion.utils.status_code import error, ErrorStatusCode, SuccessStatusCode, success

app_logging = logging.getLogger("app")


class CredentialGroup:
    _get_model_data = GetModelData(CredentialGroupModel)

    def get_credential_group(self, request):
        kwargs = request.GET.dict()
        status, message = self._get_credential_group(kwargs)
        if not status:
            app_logging.info(
                'get_credential_group, parameter：{}, error info: {}'.format((json.dumps(kwargs)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_credential_group(self, kwargs):
        id = kwargs.pop("id", None)
        all_data = kwargs.pop("all_data", None)
        if id:
            query = CredentialGroupModel.fetch_one(id=id)
            if not query:
                return False, "数据不存在"
            end_data = query.to_all_dict()
            return True, end_data
        # 全部数据
        if all_data:
            return self._get_model_data.get_all_data(kwargs)
        # 分页数据
        return self._get_model_data.get_paging_data(kwargs)

    def create_credential_group(self, request):
        data = json.loads(request.body)
        status, message = self._create_credential_group(request, data)
        if not status:
            app_logging.info(
                'create_credential_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "凭据分组", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def _create_credential_group(self, request, data):
        credential_ssh_list = data.get("credential_ssh_list", [])
        credential_password_list = data.get("credential_password_list", [])
        user_name_query = GetUserInfo().get_user_info(request)
        if not user_name_query:
            return False, "用户不存在"
        form = CredentialGroupModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        status, message = form.clean_name_unique()
        if not status:
            return False, message
        form.cleaned_data.update({"user": user_name_query})
        credential_group_query = CredentialGroupModel.create(**form.cleaned_data)
        credential_list = list(set(credential_ssh_list + credential_password_list))
        if credential_list:
            GroupCredential()._create_group_credential(
                {"credential_list": credential_list, "credential_group": credential_group_query.id})
        return True, credential_group_query.to_dict()

    def update_credential_group(self, request):
        data = json.loads(request.body)
        status, message = self._update_credential_group(data)
        if not status:
            app_logging.info(
                'update_credential_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "修改", "凭据分组", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, message))

    def _update_credential_group(self, data):
        id = data.get("id")
        credential_ssh_list = data.get("credential_ssh_list", [])
        credential_password_list = data.get("credential_password_list", [])
        form = CredentialGroupModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        credential_group_query = CredentialGroupModel.fetch_one(id=id)
        if not credential_group_query:
            return False, "分组不存在"
        credential_group_query.update(**form.cleaned_data)
        credential_list = list(set(credential_ssh_list + credential_password_list))
        if credential_list:
            GroupCredential()._create_group_credential(
                {"credential_list": credential_list, "credential_group": credential_group_query.id})
            self.update_host_credential_group_rel(credential_group_query)
        return True, credential_group_query.to_dict()

    def update_host_credential_group_rel(self, credential_group_query):
        host_list = list(set([host_credential_rel_query.host for host_credential_rel_query in
                              credential_group_query.credential_group_host.get_queryset()]))
        credential_list = list(set([credential_group_rel_query.credential for credential_group_rel_query in
                                    credential_group_query.credential_group_queryset.get_queryset()]))
        from bastion.component.resource import HostCredential
        for host in host_list:
            credential_group_rel_queryset = credential_group_query.credential_group_queryset.get_queryset()
            for credential_group_rel_query in credential_group_rel_queryset:
                HostCredential()._save_host_credential(
                    {"host": host.id, "credential": credential_group_rel_query.credential.id,
                     "credential_group": credential_group_query.id})

            for host_credential_rel_query in host.host_credential_or_credential_group.get_queryset():
                if host_credential_rel_query.credential and host_credential_rel_query.credential_group == credential_group_query:
                    if host_credential_rel_query.credential not in credential_list:
                        host_credential_rel_query.delete()
        return True, ""

    def delete_credential_group(self, request):
        data = json.loads(request.body)
        status, message = self._delete_credential_group(data)
        if not status:
            app_logging.info(
                'delete_credential_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "凭据分组", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS, message))

    def _delete_credential_group(self, data):
        id, id_list = data.get("id", None), data.get("id_list", None)
        if id:
            id_list = [id]
        for credential in id_list:
            credential_group_query = CredentialGroupModel.fetch_one(id=credential)
            if not credential_group_query:
                if id:
                    return False, "凭据分组不存在"
            credential_group_query.delete()
        return True, ""


class Credential:
    _get_model_data = GetModelData(CredentialModel)

    def get_credential(self, request):
        kwargs = request.GET.dict()
        status, message = self._get_credential(kwargs, request)
        if not status:
            app_logging.info('get_credential, parameter：{}, error info: {}'.format((json.dumps(kwargs)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_credential(self, kwargs, request=None):
        id = kwargs.pop("id", None)
        host_id = kwargs.pop("host_id", None)
        user_query = GetUserInfo().get_user_info(request)
        if not user_query:
            return False, "用户不存在"
        if user_query.role != 1:
            return self._general_get_credential_data(kwargs, user_query, host_id)
        if id:
            return self._get_model_data.get_one_data(id)

        if host_id:
            # 管理员获取当前主机全部凭据
            host_query = HostModel.fetch_one(id=host_id)
            if not host_query:
                return False, "主机不存在"
            host_all_credential_queryset = host_query.get_all_credential_queryset()
            return True, [i.to_base_dict() for i in host_all_credential_queryset]
        all_data = kwargs.pop("all_data", None)
        # 全部数据
        if all_data:
            return self._get_model_data.get_all_data(kwargs)
        # 分页数据
        return self._get_model_data.get_paging_data(kwargs)

    def _general_get_credential_data(self, kwargs, user_query, host_id):
        all_data = kwargs.pop("all_data", None)
        credential_queryset = user_query.get_user_credential_queryset()
        credential_id_list = [credential.id for credential in credential_queryset]
        if host_id:
            real_credential_queryset = list()
            host_query = HostModel.fetch_one(id=host_id)
            if not host_query:
                return False, "主机不存在"
            host_all_credential_queryset = host_query.get_all_credential_queryset()
            for credential_query in credential_queryset:
                if credential_query in host_all_credential_queryset:
                    real_credential_queryset.append(credential_query)
            return True, [i.to_base_dict() for i in real_credential_queryset]
        kwargs["id__in"] = credential_id_list
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        try:
            current, pageSize = int(kwargs.pop("current")), int(kwargs.pop("pageSize"))
        except Exception:
            current, pageSize = 1, 10
        if all_data:
            end_data = CredentialModel.fetch_all(**kwargs)
            return True, [i.to_base_dict() for i in end_data]
        current_page, total = CredentialModel.pagination(current, pageSize, **kwargs)
        end_data = [i.to_base_dict() for i in current_page]
        res_data = {
            "current": current,
            "pageSize": pageSize,
            "total": total,
            "data": end_data
        }
        return True, res_data

    def create_credential(self, request):
        data = json.loads(request.body)
        status, message = self._create_credential(request, data)
        if not status:
            app_logging.info('create_credential, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "凭据", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def _create_credential(self, request, data):
        """
        create credential
        :param data:
        {
            "name": "凭据1",
            "login_type": "auto",
            "credential_type": "password",
            "login_name": "root",
            "login_password": "123456",
            "credential_group": 1,
            "description": "description"
        }
        :return:
        {
            "code": 200,
            "successcode": 20007,
            "message": "相关信息更新成功",
            "data": {
                "id": 1,
                "name": "凭据1",
                "login_type": "auto",
                "credential_type": "password",
                "login_name": "root",
                "login_password": "123456",
                "credential_group": 1,
                "description": "description"
            }
        }
        """
        user_name_query = GetUserInfo().get_user_info(request)
        host_list = data.get("host_list", [])
        if not user_name_query:
            return False, "用户不存在"
        form = CredentialModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        status, message = form.clean_name_unique()
        if not status:
            return False, message
        form.cleaned_data.update({"user": user_name_query})
        credential_query = CredentialModel.create(**form.cleaned_data)
        if host_list:
            from bastion.component.resource import HostCredential
            HostCredential()._create_host_credential({"credential": credential_query.id, "host_list": host_list})
        return True, credential_query.to_dict()

    def update_credential(self, request):
        data = json.loads(request.body)
        status, message = self._update_credential(data)
        if not status:
            app_logging.info('update_credential, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "修改", "凭据", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, message))

    def _update_credential(self, data):
        """
        修改凭据
        :param data:
        {
            "id": 1,
            "name": "凭据1",
            "login_type": "auto",
            "credential_type": "password",
            "login_name": "root",
            "login_password": "123456",
            "credential_group": 1,
            "description": "description"
        }
        :return:
        {
            "code": 200,
            "successcode": 20007,
            "message": "相关信息更新成功",
            "data": {
                "id": 1,
                "name": "凭据1",
                "login_type": "auto",
                "credential_type": "password",
                "login_name": "root",
                "login_password": "123456",
                "credential_group": 1,
                "description": "description"
            }
        }
        """
        id = data.get("id")
        host_list = data.get("host_list")
        form = CredentialModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        cleaned_data = form.cleaned_data
        credential_type = cleaned_data.pop("credential_type", None)
        credential_query = CredentialModel.fetch_one(id=id, credential_type=credential_type)
        if not credential_query:
            return False, "凭据不存在"
        credential_query.update(**cleaned_data)
        if host_list:
            from bastion.component.resource import HostCredential
            HostCredential()._create_host_credential({"credential": credential_query.id, "host_list": host_list})
        return True, credential_query.to_dict()

    def delete_credential(self, request):
        data = json.loads(request.body)
        status, message = self._delete_credential(data)
        if not status:
            app_logging.info('delete_credential, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "凭据", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def _delete_credential(self, data):
        """
        删除凭据
        :param id: int, id_list list
        :return:
        """
        id, id_list = data.get("id", None), data.get("id_list", None)
        if id:
            id_list = [id]
        for id in id_list:
            credential_query = CredentialModel.fetch_one(id=id)
            if not credential_query:
                if id:
                    return False, "凭据不存在"
            credential_query.delete()
        return True, ""


class GroupCredential:
    def get_group_credential(self, request):
        data = request.GET.dict()
        id = data.get("id")
        relationship = CredentialGroupRelationshipModel.fetch_one(id=id)
        if relationship:
            return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, relationship.to_dict()))
        app_logging.info(
            'get_group_credential, parameter：{}, error info: {}'.format((json.dumps(data)), str("DATA_NOT_EXISTED")))
        return JsonResponse(error(ErrorStatusCode.DATA_NOT_EXISTED))

    def create_group_credential(self, request):
        data = json.loads(request.body)
        status, message = self._create_group_credential(data)
        if not status:
            app_logging.info(
                'create_group_credential, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "凭据分组关联", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS))

    def _create_group_credential(self, data):
        credential_group = data.get("credential_group")
        credential_list = data.get("credential_list", [])
        credential_group_query = CredentialGroupModel.fetch_one(id=credential_group)
        if credential_group_query:
            for credential_id in credential_list:
                form = GroupCredentialModelForm({"credential": credential_id, "credential_group": credential_group})
                if not form.is_valid():
                    continue
                CredentialGroupRelationshipModel.create(**form.cleaned_data)
            self._delete_old_data("credential_group", credential_group, "credential", credential_list)
            return True, ""
        return False, "凭据分组不存在"

    def _delete_old_data(self, old_field, old_query_id, new_field, new_query_list):
        # 删除old_queryset中不在new_query_id_list内的对象
        old_dic = {old_field: old_query_id, new_field + "__isnull": False}
        old_queryset = CredentialGroupRelationshipModel.fetch_all(**old_dic)
        new_dic = {old_field: old_query_id, new_field + "__in": new_query_list}
        new_queryset = CredentialGroupRelationshipModel.fetch_all(**new_dic)
        try:
            for old_relationship in old_queryset:
                if old_relationship not in new_queryset:
                    old_relationship.delete()
            return True, "success"
        except Exception as e:
            return False, str(e)

    def delete_group_credential(self, request):
        data = json.loads(request.body)
        status, message = self._delete_group_credential(data)
        if not status:
            app_logging.info(
                'delete_group_credential, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "凭据分组关联", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def _delete_group_credential(self, data):
        credential = data.get("credential")
        credential_group = data.get("credential_group")
        relationship = CredentialGroupRelationshipModel.fetch_one(credential=credential,
                                                                  credential_group=credential_group)
        if relationship:
            relationship.delete()
            HostCredentialRelationshipModel.objects.filter(credential=credential,
                                                           credential_group=credential_group).delete()
            return True, ""
        return False, "数据不存在"


class CommandGroup:
    _get_model_data = GetModelData(CommandGroupModel)

    def get_command_group(self, request):
        kwargs = request.GET.dict()
        status, message = self._get_command_group(kwargs)
        if not status:
            app_logging.info(
                'get_command_group, parameter：{}, error info: {}'.format((json.dumps(kwargs)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def create_command_group(self, request):
        data = json.loads(request.body)
        status, message = self._create_command_group(request, data)
        if not status:
            app_logging.info(
                'create_command_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "命令分组", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def update_command_group(self, request):
        data = json.loads(request.body)
        status, message = self._update_command_group(request, data)
        if not status:
            app_logging.info(
                'update_command_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "修改", "命令分组", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, message))

    def delete_command_group(self, request):
        data = json.loads(request.body)
        status, message = self._delete_command_group(data)
        if not status:
            app_logging.info(
                'delete_command_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "命令分组", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def _get_command_group(self, kwargs):
        id = kwargs.pop("id", None)
        all_data = kwargs.pop("all_data", None)
        if id:
            query = CommandGroupModel.fetch_one(id=id)
            if not query:
                return False, "数据不存在"
            end_data = query.to_all_dict()
            return True, end_data
        # 全部数据
        if all_data:
            return self._get_model_data.get_all_data(kwargs)
        # 分页数据
        return self._get_model_data.get_paging_data(kwargs)

    def _create_command_group(self, request, data):
        command_list = data.get("command_list", [])
        user_name_query = GetUserInfo().get_user_info(request)
        if not user_name_query:
            return False, "用户不存在"
        form = CommandGroupModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        status, message = form.clean_name_unique()
        if not status:
            return False, message
        form.cleaned_data.update({"user": user_name_query})
        command_group_query = CommandGroupModel.create(**form.cleaned_data)
        if command_list:
            GroupCommand()._create_group_command_group(
                {"command_list": command_list, "command_group": command_group_query.id})
        return True, command_group_query.to_all_dict()

    def _update_command_group(self, request, data):
        id = data.get("id")
        command_list = data.get("command_list", [])
        command_group_query = CommandGroupModel.fetch_one(id=id)
        form = CommandGroupModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        command_group_query.update(**form.cleaned_data)
        if command_list:
            GroupCommand()._create_group_command_group(
                {"command_group": command_group_query.id, "command_list": command_list})
        return True, command_group_query.to_all_dict()

    def _delete_command_group(self, data):
        id, id_list = data.get("id", None), data.get("id_list", None)
        if id:
            id_list = [id]
        for id in id_list:
            credential_query = CommandGroupModel.fetch_one(id=id)
            if not credential_query:
                if id:
                    return False, "凭据不存在"
            credential_query.delete()
            return True, ""


class Command:
    _get_model_data = GetModelData(CommandModel)

    def get_command(self, request):
        kwargs = request.GET.dict()
        status, message = self._get_command(kwargs)
        if not status:
            app_logging.info('get_command, parameter：{}, error info: {}'.format((json.dumps(kwargs)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def create_command(self, request):
        data = json.loads(request.body)
        status, message = self._create_command(request, data)
        if not status:
            app_logging.info('create_command, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "命令", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def update_command(self, request):
        data = json.loads(request.body)
        status, message = self._update_command(request, data)
        if not status:
            app_logging.info('update_command, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "修改", "命令", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, message))

    def delete_command(self, request):
        data = json.loads(request.body)
        status, message = self._delete_command(data)
        if not status:
            app_logging.info('delete_command, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "命令", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def _get_command(self, kwargs):
        id = kwargs.pop("id", None)
        all_data = kwargs.pop("all_data", None)
        if id:
            return self._get_model_data.get_one_data(id)
        # 全部数据
        if all_data:
            return self._get_model_data.get_all_data(kwargs)
        # 分页数据
        return self._get_model_data.get_paging_data(kwargs)

    def _create_command(self, request, data):
        user_name_query = GetUserInfo().get_user_info(request)
        if not user_name_query:
            return False, "用户不存在"
        command_group_list = data.get("command_group_list")
        form = CommandModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        status, message = form.clean_command_unique()
        if not status:
            return False, message
        form.cleaned_data.update({"user": user_name_query})
        command_query = CommandModel.create(**form.cleaned_data)
        if command_group_list:
            GroupCommand()._create_group_command_group(
                {"command": command_query.id, "command_group_list": command_group_list})
        return True, command_query.to_dict()

    def _update_command(self, request, data):
        id = data.get("id")
        command_group_list = data.get("command_group_list")
        command_query = CommandModel.fetch_one(id=id)
        form = CommandModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        command_query.update(**form.cleaned_data)
        if command_group_list:
            GroupCommand()._create_group_command_group(
                {"command": command_query.id, "command_group_list": command_group_list})
        return True, command_query.to_dict()

    def _delete_command(self, data):
        id, id_list = data.get("id", None), data.get("id_list", None)
        if id:
            id_list = [id]
        for id in id_list:
            credential_query = CommandModel.fetch_one(id=id)
            if not credential_query:
                if id:
                    return False, "命令不存在"
            credential_query.delete()
            return True, ""


class GroupCommand:
    def create_group_command_group(self, request):
        data = json.loads(request.body)
        status, message = self._create_group_command_group(data)
        if not status:
            app_logging.info(
                'create_group_command_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "命令分组关联", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _create_group_command_group(self, data):
        command, command_group_list = data.get("command"), data.get("command_group_list", [])
        if command and command_group_list:
            for command_group in command_group_list:
                self._save_group_command_group(command, command_group)
            self._delete_old_data("command", command, "command_group", command_group_list)
        command_group, command_list = data.get("command_group"), data.get("command_list", [])
        if command_group and command_list:
            for command in command_list:
                self._save_group_command_group(command, command_group)
            self._delete_old_data("command_group", command_group, "command", command_list)
        return True, ""

    def _save_group_command_group(self, command, command_group):
        form = GroupCommandModelForm({"command": command, "command_group": command_group})
        if form.is_valid():
            CommandGroupRelationshipModel.create(**form.cleaned_data)
            return True, ""
        return False, first_error_message(form)

    def _delete_old_data(self, old_field, old_query_id, new_field, new_query_list):
        # 删除old_queryset中不在new_query_id_list内的对象
        old_dic = {old_field: old_query_id, new_field + "__isnull": False}
        old_queryset = CommandGroupRelationshipModel.fetch_all(**old_dic)
        new_dic = {old_field: old_query_id, new_field + "__in": new_query_list}
        new_queryset = CommandGroupRelationshipModel.fetch_all(**new_dic)
        try:
            for old_relationship in old_queryset:
                if old_relationship not in new_queryset:
                    old_relationship.delete()
            return True, "success"
        except Exception as e:
            return False, str(e)

    def delete_group_command(self, request):
        data = json.loads(request.body)
        status, message = self._delete_command_group(data)
        if not status:
            app_logging.info(
                'create_group_command_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "命令分组关联", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def _delete_command_group(self, data):
        command_group = data.get("command_group")
        command = data.get("command")
        command_group_query = CommandGroupRelationshipModel.fetch_one(command_group=command_group, command=command)
        if not command_group_query:
            if id:
                return False, "数据不存在"
        command_group_query.delete()
        return True, ""


class SyncUserGroup:
    def sync_user_group(self, request):
        sync_user_and_group(request)
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS))
