from django.views import View

from bastion.component.audit import OperationLog, SessionLog, CommandLog, JsonResponse, success, SuccessStatusCode
from bastion.models import SessionCommandHistoryModel


class OperationLogView(View):
    def get(self, request):
        return OperationLog().get_operation_log(request)


class SessionLogView(View):
    def get(self, request, **kwargs):
        log_name = kwargs.get("log_name")
        type = kwargs.get("type")
        if log_name and type:
            return SessionLog().get_log_detail(**kwargs)
        return SessionLog().get_session_log(request)

    def delete(self, request):
        return SessionLog().delete_session_log(request)


class CommandLogView(View):
    def get(self, request):
        return CommandLog().get_command_log(request)


class SessionCommandHistoryView(View):
    def get(self, request):
        data = request.GET.dict()
        session_log_id = data.get("session_log_id")
        search_type = data.get("search_type")
        search_data = data.get("search_data")
        search_dict = {
            "session_log_id": session_log_id
        }
        if search_type and search_data:
            search_dict[search_type + "__contains"] = search_data
        try:
            query_set = SessionCommandHistoryModel.fetch_all(**search_dict)
            query_set = [_query_set.to_dict() for _query_set in query_set]
        except:
            query_set = []
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, query_set))
