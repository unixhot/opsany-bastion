import json
import logging

from django.http import JsonResponse

from bastion.component.audit import OperationLog
from bastion.component.common import GetModelData, GetUserInfo
from bastion.component.credential import Credential
from bastion.forms import first_error_message
from bastion.forms.forms import HostGroupModelForm, HostModelForm, HostCredentialModelForm, \
    CredentialModelForm
from bastion.models import HostModel, HostGroupModel, HostCredentialRelationshipModel, UserInfo, UserGroupModel, CredentialGroupRelationshipModel
from bastion.utils.status_code import success, SuccessStatusCode, error, ErrorStatusCode

app_logging = logging.getLogger("app")


class HostGroup:
    _get_model_data = GetModelData(HostGroupModel)
    def get_host_group(self, request, **kwargs):
        data = request.GET.dict()
        user_query = GetUserInfo().get_user_info(request)
        group_type = kwargs.get('group_type')
        if group_type == HostGroupModel.RESOURCE_DATABASE:
            data["group_type"] = HostGroupModel.RESOURCE_DATABASE
        else:
            data["group_type"] = HostGroupModel.RESOURCE_HOST
        id = data.get("id")
        all_data = data.pop("all_data", None)
        # 单条数据
        if id:
            return self._get_one_data(id, request)
        # 全部数据
        # if all_data:
        return self._get_all_data(data, user_query)

    def _get_one_data(self, id, request=None):
        host_group_query = HostGroupModel.fetch_one(id=id)
        if not host_group_query:
            return JsonResponse(error(ErrorStatusCode.HOST_GROUP_NOT_EXISTED))
        res_data = host_group_query.to_parent_host_dict()
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, res_data))

    def _get_all_data(self, kwargs, user_query=None):
        kwargs["parent"] = None
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__icontains"] = search_data
        credential_group_queryset = HostGroupModel.fetch_all(**kwargs).order_by("create_time")
        end_data = []
        if credential_group_queryset:
            for i in credential_group_queryset:
                end_data.append(i.to_parent_dict(user_query))
        if user_query.role not in [1]:
            end_data = self.clean_parent_dict(end_data)
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))

    def clean_parent_dict(self, li: list):
        # 删除分组下没有主机的数据
        for i in range(len(li)-1, -1, -1):
            dic = li[i]
            if dic.get("count") == 0:
                li.pop(i)
            else:
                self.clean_parent_dict(dic.get("children", []))
        return li

    def get_host_group_console(self, request):
        kwargs = request.GET.dict()
        search_data = kwargs.pop("search_data", {})
        user_query = GetUserInfo().get_user_info(request)
        if not user_query:
            return False, "用户不存在"
        host_status, host_message = self._get_host_group_console(user_query, search_data, group_type="host")
        database_status, database_message = self._get_host_group_console(user_query, search_data, group_type="database")
        if not host_status:
            app_logging.info('get_host_group_console, parameter：{}, error info: {}'.format((json.dumps(kwargs)), str(host_message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=host_message))
        if not database_status:
            app_logging.info('get_host_group_console, parameter：{}, error info: {}'.format((json.dumps(kwargs)), str(database_message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=database_message))
        host_count = sum([host.get("count") for host in host_message])
        database_count = sum([host.get("count") for host in database_message])
        res_list = [
            {
                "name": "主机资源",
                "group_type": "host",
                "key": "host_group_parent",
                "type": "group",
                "count": host_count,
                "children": host_message
            },
            {
                "name": "数据库资源",
                "group_type": "database",
                "key": "database_group_parent",
                "type": "group",
                "count": database_count,
                "children": database_message
            },
        ]
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, res_list))

    def _get_host_group_console(self, user_query, search_data=None, group_type="host"):
        all_host_group_queryset = HostGroupModel.fetch_all(parent=None, group_type=group_type).order_by("create_time")
        if user_query.role != 1:
            # 获取到当前用户通过授权的主机，传入to_all_dict用以标识是否不可点击（控制台会出现有主机但是时间限制无法登录情况）
            host_queryset_v2 = user_query.get_user_host_queryset_v2()
            host_list = [host_group.to_all_dict(user_query, search_data, user=user_query, host_queryset_v2=host_queryset_v2) for host_group in all_host_group_queryset]
            host_list = self.clean_parent_dict(host_list)
        else:
            host_list = [host_group.to_all_dict(search_data=search_data, user=user_query) for host_group in all_host_group_queryset]
        return True, host_list

    def create_host_group(self, request, **kwargs):
        data = json.loads(request.body)
        group_type = kwargs.get('group_type')
        if group_type == HostGroupModel.RESOURCE_DATABASE:
            data["group_type"] = HostGroupModel.RESOURCE_DATABASE
        else:
            data["group_type"] = HostGroupModel.RESOURCE_HOST
        status, message = self._create_host_group(request, data)
        if not status:
            app_logging.info('create_host_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "资源分组", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def _create_host_group(self, request, data):
        user_name_query = GetUserInfo().get_user_info(request)
        if not user_name_query:
            return False, "用户不存在"
        data.update({"user": user_name_query.id})
        form = HostGroupModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        status, message = form.clean_name_unique()
        if not status:
            return False, message
        form.cleaned_data.update({"user": user_name_query})
        host_group_query = HostGroupModel.create(**form.cleaned_data)
        return True, host_group_query.to_dict()

    def update_host_group(self, request, **kwargs):
        data = json.loads(request.body)
        group_type = kwargs.get('group_type')
        if group_type == HostGroupModel.RESOURCE_DATABASE:
            data["group_type"] = HostGroupModel.RESOURCE_DATABASE
        else:
            data["group_type"] = HostGroupModel.RESOURCE_HOST
        if not data.get("group_type"):
            data["group_type"] = HostGroupModel.RESOURCE_HOST
        status, message = self._update_host_group(data, request)
        if not status:
            app_logging.info('update_host_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "修改", "资源分组", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, message))

    def _update_host_group(self, data, request):
        id = data.get("id")
        host_group_query = HostGroupModel.fetch_one(id=id)
        if not host_group_query:
            return False, "用户不存在"
        form = HostGroupModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        form.cleaned_data.pop("parent", None)
        host_group_query = host_group_query.update(**form.cleaned_data)
        return True, host_group_query.to_dict()

    def delete_host_group(self, request, **kwargs):
        data = json.loads(request.body)
        group_type = kwargs.get('group_type')
        if group_type == HostGroupModel.RESOURCE_DATABASE:
            data["group_type"] = HostGroupModel.RESOURCE_DATABASE
        else:
            data["group_type"] = HostGroupModel.RESOURCE_HOST
        status, message = self._delete_host_group(data)
        if not status:
            app_logging.info('delete_host_group, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "资源分组", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def _delete_host_group(self, data):
        id, id_list = data.get("id", None), data.get("id_list", None)
        group_type = data.get("group_type", None)
        # if id:
        #     id_list = [id]
        # for host_group_id in id_list:
        #     host_group_query = HostGroupModel.fetch_one(id=host_group_id)
        #     if not host_group_query:
        #         if id:
        #             return False, "分组不存在"
        #     status, message = HostGroupModelForm().check_delete(id)
        #     if not status:
        #         if id:
        #             return False, message
        if not id:
            return False, "参数错误"
        host_group_query = HostGroupModel.fetch_one(id=id, group_type=group_type)
        if not host_group_query:
            return False, "资源分组不存在"
        host_query = HostModel.fetch_one(group=host_group_query)
        if host_query:
            return False, "当前分组下有关联资源无法删除"
        if host_group_query.check_host_dict():
            return False, "当前分组的子分组下有关联资源无法删除"
        host_group_query.delete()
        return True, ""


class Host:
    _get_model_data = GetModelData(HostModel)

    def get_host(self, request, **kwargs):
        data = request.GET.dict()
        resource_type = kwargs.get('resource_type')
        if resource_type == HostModel.RESOURCE_DATABASE:
            data["resource_type"] = HostModel.RESOURCE_DATABASE
        else:
            data["resource_type"] = HostModel.RESOURCE_HOST
        status, message = self._get_host(data, request)
        if not status:
            app_logging.info('get_host, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_host(self, kwargs, request=None):
        user_query = GetUserInfo().get_user_info(request)
        if not user_query:
            return False, "用户不存在"
        id = kwargs.pop("id", None)
        all_data = kwargs.pop("all_data", None)
        network_proxy = kwargs.pop("network_proxy", None)
        if network_proxy:
            kwargs["network_proxy"] = None
            return self._get_netwok_proxy_data(kwargs, user_query)
        if id:
            return self._get_one_data(id, user_query)
        # 全部数据
        if all_data:
            return self._get_all_data(kwargs, user_query)
        # 分页数据
        return self._get_paging_data(kwargs, user_query)

    def _get_one_data(self, id, user_query):
        if user_query.role != 1:
            host_queryset = user_query.get_user_host_queryset_v2()
            host_id_list = [host.id for host in host_queryset]
            if int(id) not in host_id_list:
                return False, "无权访问该资源"
        query = HostModel.fetch_one(id=id)
        if not query:
            return False, "数据不存在"
        end_data = query.get_all_dict()
        return True, end_data

    def _get_all_data(self, kwargs, user_query):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        group_id = kwargs.get("group_id")
        if group_id:
            host_group_query = HostGroupModel.fetch_one(id=group_id)
            if host_group_query:
                kwargs.pop("group_id", None)
                kwargs["group__in"] = host_group_query.get_children_group_queryset()
        if user_query.role != 1:
            host_queryset = user_query.get_user_host_queryset_v2()
            host_id_list = [host.id for host in host_queryset]
            kwargs["id__in"] = host_id_list
        resource_queryset = HostModel.fetch_all(**kwargs)
        end_data = []
        if resource_queryset:
            for i in resource_queryset:
                end_data.append(i.to_dict())
        return True, end_data

    def _get_paging_data(self, kwargs, user_query):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        try:
            current, pageSize = int(kwargs.pop("current")), int(kwargs.pop("pageSize"))
        except Exception:
            current, pageSize = 1, 10
        group_id = kwargs.get("group_id")
        if group_id:
            host_group_query = HostGroupModel.fetch_one(id=group_id)
            if host_group_query:
                kwargs.pop("group_id", None)
                print("host_group_query", host_group_query.get_children_group_queryset())
                kwargs["group__in"] = host_group_query.get_children_group_queryset()
        if user_query.role != 1:
            host_queryset = user_query.get_user_host_queryset_v2()
            host_id_list = [host.id for host in host_queryset]
            kwargs["id__in"] = host_id_list
        current_page, total = HostModel.pagination(current, pageSize, **kwargs)
        end_data = [i.to_dict() for i in current_page]
        res_data = {
            "current": current,
            "pageSize": pageSize,
            "total": total,
            "data": end_data
        }
        return True, res_data

    def _get_netwok_proxy_data(self, kwargs, user_query):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        if user_query.role == 1:
            resource_queryset = HostModel.fetch_all(**kwargs)
            return True, [resource_query.to_network_proxy_dict() for resource_query in resource_queryset]
        return False, "您无权访问"

    def _get_host_paging_data(self, kwargs):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        try:
            current, pageSize = int(kwargs.pop("current")), int(kwargs.pop("pageSize"))
        except Exception:
            current, pageSize = 1, 10
        current_page, total = HostModel.pagination(current, pageSize, **kwargs)
        end_data = [i.get_all_dict() for i in current_page]
        res_data = {
            "current": current,
            "pageSize": pageSize,
            "total": total,
            "data": end_data
        }
        return True, res_data

    def create_host(self, request, **kwargs):
        """

        :param request:
        {
            "host_name": "测试创建资源凭据2",
            "system_type": "Linux",
            "protocol_type": "SSH",
            "host_address": "www.hu27.cn",
            "port": 22,
            "group": 1,
            "credential_list": [1,2,3,4],
            "credential_group_list": [1,2,3,4],
            "credential": {
                "name": "测试创建资源凭据3",
                "login_type": "auto",
                "credential_type": "password",
                "login_name": "root",
                "login_password": "123456"
            }
        }

        :return:
        """
        data = json.loads(request.body)
        if not data.get("resource_type"):
            data["resource_type"] = HostModel.RESOURCE_HOST
        resource_type = kwargs.get('resource_type')
        if resource_type == HostModel.RESOURCE_DATABASE:
            data["resource_type"] = HostModel.RESOURCE_DATABASE
            data["system_type"] = HostModel.SYSTEM_LINUX
            data["protocol_type"] = HostModel.PROTOCOL_SSH
        else:
            data["resource_type"] = HostModel.RESOURCE_HOST
        status, message = self._create_host(request, data)
        if not status:
            app_logging.info('create_host, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "资源", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def _create_host(self, request, data):
        credential = data.pop("credential", {})
        import copy
        original_credential = copy.deepcopy(credential)
        credential_list = data.pop("credential_list", [])
        credential_group_list = data.pop("credential_group_list", [])
        form = HostModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        host_name_code = form.cleaned_data.get("host_name_code")
        if HostModel.fetch_one(host_name_code=host_name_code):
            return False, "唯一标识已存在"
        status, message = form.clean_host_name_unique()
        if not status:
            return False, message
        if credential:
            form_credential = CredentialModelForm(credential)
            if not form_credential.is_valid():
                return False, first_error_message(form_credential)
            status, message = form_credential.clean_name_unique()
            if not status:
                return False, message

        user_name_query = GetUserInfo().get_user_info(request)
        if not user_name_query:
            return False, "用户不存在"
        form.cleaned_data.update({"user": user_name_query})
        host_query = HostModel.create(**form.cleaned_data)
        if credential:
            status, credential_message = Credential()._create_credential(request, original_credential)
            if status:
                HostCredential()._create_host_credential(
                    {"host": host_query.id, "credential_list": [credential_message.get("id")]})
                credential_list.append(credential_message.get("id"))
        HostCredential()._create_host_credential({
            "host": host_query.id, "credential_list":
                credential_list, "credential_group_list":
                credential_group_list})
        return True, host_query.to_dict()

    def _add_host_credential(self, request, host, credential):
        status, message = Credential()._create_credential(request, credential)
        if not status:
            return False, message
        return HostCredential()._create_host_credential({"host": host, "credential_list": [message.get("id")]})

    def update_host(self, request, **kwargs):
        data = json.loads(request.body)
        if not data.get("resource_type"):
            data["resource_type"] = HostModel.RESOURCE_HOST
        resource_type = kwargs.get('resource_type')
        if resource_type == HostModel.RESOURCE_DATABASE:
            data["resource_type"] = HostModel.RESOURCE_DATABASE
            data["system_type"] = HostModel.SYSTEM_LINUX
            data["protocol_type"] = HostModel.PROTOCOL_SSH
        else:
            data["resource_type"] = HostModel.RESOURCE_HOST
        status, message = self._update_host(request, data)
        if not status:
            app_logging.info('update_host, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "修改", "资源", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, message))

    def _update_host(self, request, data):
        id = data.get("id")
        credential_list = data.get("credential_list", [])
        credential_group_list = data.get("credential_group_list", [])
        host_query = HostModel.fetch_one(id=id)
        if not host_query:
            return JsonResponse(error(ErrorStatusCode.RECORD_HAS_EXISTED))
        form = HostModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        # form.cleaned_data.pop("host_name_code", None)
        host_query = host_query.update(**form.cleaned_data)
        HostCredential()._create_host_credential({
            "host": host_query.id,
            "credential_list": credential_list,
            "credential_group_list": credential_group_list})
        return True, host_query.to_dict()

    def delete_host(self, request, **kwargs):
        data = json.loads(request.body)
        resource_type = kwargs.get('resource_type')
        if resource_type == HostModel.RESOURCE_DATABASE:
            data["resource_type"] = HostModel.RESOURCE_DATABASE
        else:
            data["resource_type"] = HostModel.RESOURCE_HOST
        status, message = self._delete_host(data)
        if not status:
            app_logging.info('delete_host, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "资源", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def _delete_host(self, data):
        id, id_list = data.get("id", None), data.get("id_list", None)
        resource_type = data.get("resource_type", None)
        if id:
            id_list = [id]
        for host_id in id_list:
            host_query = HostModel.fetch_one(id=host_id, resource_type=resource_type)
            if not host_query:
                if id:
                    return False, "资源不存在"
            host_query.delete()
        return True, ""


class AuthHost:
    def get_auth_host(self, request):
        kwargs = request.GET.dict()
        user_query = GetUserInfo().get_user_info(request)
        if not user_query:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="用户不存在"))
        status, message = self._get_auth_host(kwargs, user_query)
        if not status:
            app_logging.info('get_host, parameter：{}, error info: {}'.format((json.dumps(kwargs)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_auth_host(self, kwargs, user_query):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        try:
            current, pageSize = int(kwargs.pop("current")), int(kwargs.pop("pageSize"))
        except Exception:
            current, pageSize = 1, 10
        group_id = kwargs.get("group_id")
        if group_id:
            host_group_query = HostGroupModel.fetch_one(id=group_id)
            if host_group_query:
                kwargs.pop("group_id", None)
                # print("host_group_query", host_group_query.get_children_group_queryset())
                kwargs["group__in"] = host_group_query.get_children_group_queryset()
        host_queryset_v2 = user_query.get_user_host_queryset_v2()
        if user_query.role != 1:
            host_queryset_v3 = user_query.get_user_host_queryset_v3()
            host_id_list = [host.id for host in host_queryset_v3]
            kwargs["id__in"] = host_id_list
        current_page, total = HostModel.pagination(current, pageSize, **kwargs)
        end_data = []
        for host in current_page:
            dic = host.to_auth_host_dict()
            if user_query.role != 1:
                if host not in host_queryset_v2:
                    dic["time_frame"] = False
                else:
                    dic["time_frame"] = True
            else:
                dic["time_frame"] = True
            end_data.append(dic)
        res_data = {
            "current": current,
            "pageSize": pageSize,
            "total": total,
            "data": end_data
        }
        return True, res_data


class AuthResource:
    def get_auth_resource(self, request, **kwargs):
        data = request.GET.dict()
        resource_type = kwargs.get('resource_type')
        if resource_type == HostModel.RESOURCE_DATABASE:
            data["resource_type"] = HostModel.RESOURCE_DATABASE
        else:
            data["resource_type"] = HostModel.RESOURCE_HOST
        user_query = GetUserInfo().get_user_info(request)
        if not user_query:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="用户不存在"))
        status, message = self._get_auth_resource(data, user_query)
        if not status:
            app_logging.info('get_host, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_auth_resource(self, kwargs, user_query):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        try:
            current, pageSize = int(kwargs.pop("current")), int(kwargs.pop("pageSize"))
        except Exception:
            current, pageSize = 1, 10
        group_id = kwargs.get("group_id")
        if group_id:
            host_group_query = HostGroupModel.fetch_one(id=group_id)
            if host_group_query:
                kwargs.pop("group_id", None)
                kwargs["group__in"] = host_group_query.get_children_group_queryset()
        host_queryset_v2 = user_query.get_user_host_queryset_v2()
        if user_query.role != 1:
            host_queryset_v3 = user_query.get_user_host_queryset_v3()
            host_id_list = [host.id for host in host_queryset_v3]
            kwargs["id__in"] = host_id_list
        current_page, total = HostModel.pagination(current, pageSize, **kwargs)
        end_data = []
        for host in current_page:
            dic = host.to_auth_host_dict()
            if user_query.role != 1:
                if host not in host_queryset_v2:
                    dic["time_frame"] = False
                else:
                    dic["time_frame"] = True
            else:
                dic["time_frame"] = True
            end_data.append(dic)
        res_data = {
            "current": current,
            "pageSize": pageSize,
            "total": total,
            "data": end_data
        }
        return True, res_data



class HostCredential:
    def get_host_credential(self, request):
        data = request.GET.dict()
        id = data.get("id")
        relationship = HostCredentialRelationshipModel.fetch_one(id=id)
        if relationship:
            return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, relationship.to_dict()))
        return JsonResponse(error(ErrorStatusCode.DATA_NOT_EXISTED))

    def create_host_credential(self, request):
        data = json.loads(request.body)
        status, message = self._create_host_credential(data)
        if not status:
            app_logging.info(
                'create_host_credential, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "资源凭据", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def _create_host_credential(self, data):
        """
        资源关联凭据，凭据分组，凭据关联资源，凭据分组关联资源
        host: 1
        host_list: [1,2,3]
        credential: [1,2,3]
        credential_list: [1,2,3]
        credential_group: [query, query]
        credential_group_list: [query, query]
        """
        host, credential_list, credential_group_list = data.get("host"), data.get("credential_list", []), data.get(
            "credential_group_list", [])
        credential, credential_group, host_list = data.get("credential"), data.get("credential_group"), data.get(
            "host_list", [])
        if host:
            for credential_id in credential_list:
                self._save_host_credential({"host": host, "credential": credential_id})
            self._delete_old_data("host", host, "credential", credential_list, other={"credential_group__isnull": True})
            for credential_group_id in credential_group_list:
                credential_group_rel_queryset = CredentialGroupRelationshipModel.fetch_all(credential_group_id=credential_group_id)
                for credential_group_rel_query in credential_group_rel_queryset:
                    self._save_host_credential({"host": host, "credential":credential_group_rel_query.credential.id, "credential_group": credential_group_id})
            self._delete_old_data("host", host, "credential_group", credential_group_list, other={"credential__isnull": False})
        if credential:
            for host_id in host_list:
                self._save_host_credential({"host": host_id, "credential": credential})
            self._delete_old_data("credential", credential, "host", host_list, other={"credential_group__isnull": True})
        if credential_group:
            for host_id in host_list:
                credential_group_rel_queryset = credential_group.credential_group_queryset.get_queryset()
                for credential_group_rel_query in credential_group_rel_queryset:
                    self._save_host_credential({"host": host_id, "credential":credential_group_rel_query.credential.id, "credential_group": credential_group.id})
            self._delete_old_data("credential_group", credential_group, "host", host_list, other={"credential__isnull": False})

        return True, ""

    def _save_host_credential(self, data):
        form = HostCredentialModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        relationship, _ = HostCredentialRelationshipModel.objects.get_or_create(**form.cleaned_data)
        return True, relationship.to_dict()

    def _delete_old_data(self, old_field, old_query_id, new_field, new_query_list, other=None):
        # 删除old_queryset中不在new_query_id_list内的对象
        old_dic = {old_field: old_query_id, new_field + "__isnull": False}
        if other: old_dic.update(other)
        old_queryset = HostCredentialRelationshipModel.fetch_all(**old_dic)
        new_dic = {old_field: old_query_id, new_field + "__in": new_query_list}
        if other: new_dic.update(other)
        new_queryset = HostCredentialRelationshipModel.fetch_all(**new_dic)
        try:
            for old_relationship in old_queryset:
                if old_relationship not in new_queryset:
                    old_relationship.delete()
            return True, "success"
        except Exception as e:
            return False, str(e)

    def delete_host_credential(self, request):
        data = json.loads(request.body)
        status, message = self._delete_host_credential(data)
        if not status:
            app_logging.info(
                'delete_host_credential, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "资源凭据", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS, message))

    def _delete_host_credential(self, data):
        host = data.get("host")
        credential = data.get("credential")
        credential_group = data.get("credential_group")
        if host and credential:
            HostCredentialRelationshipModel.objects.filter(host=host, credential=credential,credential_group__isnull=True).delete()
            return True, ""
        if host and credential_group:
            HostCredentialRelationshipModel.objects.filter(host=host, credential_group=credential_group).delete()
            return True, ""
        return False, "数据不存在"


class User:
    _get_model_data = GetModelData(UserInfo)

    def get_user_info(self, request):
        kwargs = request.GET.dict()
        status, message = self._get_user_info(kwargs)
        if not status:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_user_info(self, kwargs):
        id = kwargs.pop("id", None)
        all_data = kwargs.pop("all_data", None)
        if id:
            return self._get_model_data.get_one_data(id)
        # 非管理员数据
        kwargs.update({"role__in": [0, 2]})
        if all_data:
            return self._get_model_data.get_all_data(kwargs)
        # 分页数据
        return self._get_model_data.get_paging_data(kwargs)


class UserGroup:
    _get_model_data = GetModelData(UserGroupModel)

    def get_user_group_info(self, request):
        kwargs = request.GET.dict()
        status, message = self._get_user_group_info(kwargs)
        if not status:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_user_group_info(self, kwargs):
        id = kwargs.pop("id", None)
        all_data = kwargs.pop("all_data", None)
        if id:
            return self._get_model_data.get_one_data(id)
        # 全部数据
        if all_data:
            return self._get_model_data.get_all_data(kwargs)
        # 分页数据
        return self._get_model_data.get_paging_data(kwargs)
