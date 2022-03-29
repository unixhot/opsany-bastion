import time
import datetime
from django.utils import timezone
import json
import logging
import os

from django.http import JsonResponse, HttpResponse

from django.conf import settings
from bastion.component.common import GetModelData, GetUserInfo
from bastion.models import OperationLogModel, SessionLogModel, CommandLogModel, SessionLogInfoModel
from bastion.utils.esb_api import EsbApi
from bastion.utils.status_code import success, SuccessStatusCode, ErrorStatusCode, error
from bastion.core.terminal.component import SSHBaseComponent

app_logging = logging.getLogger("app")


class OperationLog:
    _get_model_data = GetModelData(OperationLogModel)

    def get_operation_log(self, request):
        data = request.GET.dict()
        status, message = self._get_operation_log(data)
        if not status:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_operation_log(self, data):
        id = data.pop("id", None)
        all_data = data.pop("all_data", None)
        if id:
            return self._get_model_data.get_one_data(id)
        # 全部数据
        if all_data:
            return self._get_model_data.get_all_data(data)
        # 分页数据
        return self._get_model_data.get_paging_data(data)

    @classmethod
    def request_log(cls, request, operation_type, operation_object, operation_content):
        method = request.method
        try:
            data = json.loads(request.body)
        except:
            data = {}
        parameter = {
            "params": request.GET.dict(),
            "data": data,
            "form": request.POST.dict()
        }
        bk_token = request.COOKIES.get("bk_token")
        esb_obj = EsbApi(bk_token)
        user_info = esb_obj.get_user_info()
        username = user_info.get("username")
        operation_log_data = {
            "username": username or "operator",
            'operation_type': operation_type,
            'operation_object': operation_object,
            'operation_content': operation_content,
            'parameter': parameter,
            "method": method
        }
        OperationLogModel.create(**operation_log_data)
        return True, ""


class SessionLog:
    _get_model_data = GetModelData(SessionLogModel)

    def get_session_log(self, request):
        data = request.GET.dict()
        finished = data.pop("finished", None)
        user_query = GetUserInfo().get_user_info(request)
        if not user_query:
            return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS))
        if user_query.role != 1:
            data["user"] = user_query.username
        if finished:
            data["is_finished"] = True
        else:
            data["is_finished"] = False
        status, message = self._get_session_log(data)
        if not status:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_session_log(self, data):
        id = data.pop("id", None)
        all_data = data.pop("all_data", None)
        if id:
            return self._get_model_data.get_one_data(id)
        # 全部数据
        if all_data:
            return self._get_model_data.get_all_data(data)
        # 分页数据
        return self._get_model_data.get_paging_data(data)

    def get_log_detail(self, **kwargs):
        log_name = kwargs.get("log_name", "")
        type = kwargs.get("type")
        status, message = self._get_log_detail(type, log_name)
        if not status:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        if status == 1:
            return JsonResponse(message)
        return HttpResponse(message)

    def _get_log_detail(self, type, log_name):
        if type == "guacamole":
            file_path = os.path.join(settings.ORI_GUACD_PATH, "logfile")
        elif type == "terminal":
            log_name += ".log"
            log_query = SessionLogInfoModel.fetch_one(log_name=log_name)
            if not log_query:
                file_path = settings.TERMINAL_PATH
            else:
                return 1, log_query.info
        else:
            return False, '会话信息不存在!'
        full_path = os.path.join(file_path, log_name)
        if not os.path.exists(full_path):
            return False, '会话信息不存在'
        else:
            print("full_path", full_path)
            with open(full_path, 'r') as f:
                file_data = f.read()
            if type == "terminal":
                return 1, json.loads(file_data)
            return 2, file_data

    def delete_session_log(self, request):
        data = json.loads(request.body)
        status, message = self._kill_session(data)
        if not status:
            app_logging.info('kill_session_log, parameter：{}, error info: {}'.format((json.dumps(data)), str(message)))
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        OperationLog.request_log(request, "删除", "强制下线", "success")
        return JsonResponse(success(SuccessStatusCode.OPERATION_SUCCESS, custom_message=message))

    def _kill_session(self, data):
        session_list = data.get("session_list", [])
        success_count, error_count = 0, 0
        for session in session_list:
            channel = session.get('channel', None)
            log_name = session.get('log_name', None)
            session_query = SessionLogModel.fetch_one(channel=channel, log_name=log_name)
            if not session_query:
                error_count += 1
                continue
            if session_query.is_finished:
                error_count += 1
                continue
            else:
                try:
                    session_query.update(**{
                        "end_time": datetime.datetime.now(),
                        "is_finished": True
                    })
                    queue = SSHBaseComponent().get_redis_instance()
                    queue.publish(channel, json.dumps(['close']))
                    success_count += 1
                except:
                    pass
        if len(session_list) == 1 and error_count == 1:
            return False, "会话不存在"
        message = "成功关闭{}台， 失败{}台！".format(success_count, error_count)
        return True, message


class CommandLog:
    _get_model_data = GetModelData(CommandLogModel)

    def get_command_log(self, request):
        data = request.GET.dict()
        status, message = self._get_command_log(data)
        if not status:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message=message))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, message))

    def _get_command_log(self, data):
        id = data.pop("id", None)
        all_data = data.pop("all_data", None)
        if id:
            return self._get_model_data.get_one_data(id)
        # 全部数据
        if all_data:
            return self._get_model_data.get_all_data(data)
        # 分页数据
        return self._get_model_data.get_paging_data(data)
