import json
import logging

from django.http import JsonResponse

from bastion.component.audit import OperationLog
from bastion.component.common import GetModelData, GetUserInfo
from bastion.forms import first_error_message
from bastion.forms.network_proxy_form import NetworkProxyModelForm
from bastion.models import HostModel, NetworkProxyModel
from bastion.utils.status_code import success, SuccessStatusCode, error, ErrorStatusCode

app_logging = logging.getLogger("app")


class NetworkProxy:
    _get_model_data = GetModelData(HostModel)

    def get_network_proxy(self, request):
        data = request.GET.dict()
        status, message = self._get_network_proxy(data, request)
        if not status:
            app_logging.info('get_network_proxy, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_network_proxy(self, kwargs, request=None):
        user_query = GetUserInfo().get_user_info(request)
        if not user_query:
            return False, "用户不存在"
        id = kwargs.pop("id", None)
        all_data = kwargs.pop("all_data", None)
        if id:
            return self._get_one_data(id)
        # 全部数据
        if all_data:
            return self._get_all_data(kwargs)
        # 分页数据
        return self._get_paging_data(kwargs)

    def _get_one_data(self, id):
        query = NetworkProxyModel.fetch_one(id=id)
        if not query:
            return False, "数据不存在"
        end_data = query.to_dict()
        return True, end_data

    def _get_all_data(self, kwargs):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        network_proxy_queryset = NetworkProxyModel.fetch_all(**kwargs)
        end_data = [i.to_dict() for i in network_proxy_queryset]
        return True, end_data

    def _get_paging_data(self, kwargs):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        try:
            current, pageSize = int(kwargs.pop("current")), int(kwargs.pop("pageSize"))
        except Exception:
            current, pageSize = 1, 10
        current_page, total = NetworkProxyModel.pagination(current, pageSize, **kwargs)
        end_data = [i.to_dict() for i in current_page]
        res_data = {
            "current": current,
            "pageSize": pageSize,
            "total": total,
            "data": end_data
        }
        return True, res_data

    def create_network_proxy(self, request):
        data = json.loads(request.body)
        status, message = self._create_network_proxy(request, data)
        if not status:
            app_logging.info(
                'create_network_proxy, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "网络代理", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def _create_network_proxy(self, request, data):
        if NetworkProxyModel.fetch_one(name=data.get("name")):
            return False, "网络协议已存在"
        form = NetworkProxyModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        user_name_query = GetUserInfo().get_user_info(request)
        if not user_name_query:
            return False, "用户不存在"
        form.cleaned_data.update({"user": user_name_query})
        network_proxy_query = NetworkProxyModel.create(**form.cleaned_data)
        return True, network_proxy_query.to_dict()

    def update_network_proxy(self, request):
        data = json.loads(request.body)
        status, message = self._update_network_proxy(data)
        if not status:
            app_logging.info(
                'update_network_proxy, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "修改", "网络代理", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, message))

    def _update_network_proxy(self, data):
        id = data.get("id")
        network_proxy_query = NetworkProxyModel.fetch_one(id=id)
        if not network_proxy_query:
            return False, "数据不存在"
        form = NetworkProxyModelForm(data)
        if not form.is_valid():
            return False, first_error_message(form)
        network_proxy_query = network_proxy_query.update(**form.cleaned_data)
        return True, network_proxy_query.to_dict()

    def delete_network_proxy(self, request):
        data = json.loads(request.body)
        status, message = self._delete_network_proxy(data)
        if not status:
            app_logging.info(
                'delete_network_proxy, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "网络代理", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def _delete_network_proxy(self, data):
        id, id_list = data.get("id", None), data.get("id_list", None)
        if id:
            id_list = [id]
        for network_proxy_id in id_list:
            network_proxy_query = NetworkProxyModel.fetch_one(id=network_proxy_id)
            if not network_proxy_query:
                if id:
                    return False, "资源不存在"
            if HostModel.fetch_all(network_proxy=network_proxy_query):
                if id:
                    return False, "请先解除本代理上的资源绑定，方可删除。"
                continue
            network_proxy_query.delete()
        return True, ""


class NetworkProxyResource:
    def get_network_proxy_resource(self, request):
        kwargs = request.GET.dict()
        status, message = self._get_network_proxy_resource(kwargs)
        if not status:
            app_logging.info(
                'get_network_proxy_resource, parameter：{}, error info: {}'.format((json.dumps(kwargs)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def create_network_proxy_resource(self, request):
        data = json.loads(request.body)
        status, message = self._create_network_proxy_resource(data)
        if not status:
            app_logging.info(
                'create_network_proxy_resource, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "新建", "网络代理关联资源", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS, message))

    def delete_network_proxy_resource(self, request):
        data = json.loads(request.body)
        status, message = self._delete_network_proxy_resource(data)
        if not status:
            app_logging.info(
                'delete_network_proxy_resource, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "网络代理取消关联资源", "success")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS, message))

    def _get_network_proxy_resource(self, kwargs):
        network_proxy_id, resource_type = kwargs.get("network_proxy_id"), kwargs.get("resource_type", "host")
        if not network_proxy_id:
            return False, "缺失参数"
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        dic = {}
        if search_type and search_data:
            dic[search_type + "__contains"] = search_data
        try:
            current, pageSize = int(kwargs.pop("current")), int(kwargs.pop("pageSize"))
        except Exception:
            current, pageSize = 1, 5
        current_page, total = HostModel.pagination(current, pageSize, network_proxy_id=network_proxy_id,
                                                   resource_type=resource_type, **dic)
        end_data = [i.to_network_proxy_dict() for i in current_page]
        res_data = {
            "current": current,
            "pageSize": pageSize,
            "total": total,
            "data": end_data
        }
        return True, res_data

    def _create_network_proxy_resource(self, data):
        network_proxy_id = data.get("network_proxy_id")
        resource_list = data.get("resource_list")
        network_proxy_query = NetworkProxyModel.fetch_one(id=network_proxy_id)
        if not network_proxy_query:
            return False, "网络代理不存在"
        new_resource_query_list = list()
        for resource_id in resource_list:
            query = HostModel.fetch_one(id=resource_id)
            if query:
                if not query.network_proxy or query.network_proxy == network_proxy_query:
                    new_resource_query_list.append(query)
        if not new_resource_query_list:
            return False, "选择的资源不存在或资源已关联网络代理"
        for resource_query in new_resource_query_list:
            resource_query.update(network_proxy=network_proxy_query)
        return True, "关联成功"

    def _delete_network_proxy_resource(self, data):
        network_proxy_id = data.get("network_proxy_id")
        resource_id = data.get("resource_id")
        network_proxy_query = NetworkProxyModel.fetch_one(id=network_proxy_id)
        if not network_proxy_query:
            return False, "网络代理不存在"
        resource_query = HostModel.fetch_one(id=resource_id, network_proxy=network_proxy_query)
        if not resource_query:
            return False, "选择的资源不存在或资源已关联其他网络代理"
        resource_query.update(network_proxy=None)
        return True, "资源关联移除成功"
