from django.views import View
from django.http import JsonResponse

from bastion.component.common import GetUserInfo
from bastion.utils.status_code import success, SuccessStatusCode, error, ErrorStatusCode
from bastion.utils.iam import Permission
from bastion.utils.esb_api import EsbApi
from bastion.models import HostModel, CredentialModel, StrategyAccessModel, StrategyCommandModel, SessionLogModel


class GetInfoForWorkbenchView(View):
    def get(self, request):
        user_query = GetUserInfo().get_user_info(request)
        host_count, database_count = 0, 0
        session_unfinished_count, session_finished_count = 0, 0
        strategy_access_count, strategy_command_count = 0, 0
        credential_password_count, credential_ssh_count = 0, 0
        if user_query:
            if user_query.role != 1:
                host_count = len(user_query.get_user_host_queryset_v2())
                session_finished_count = SessionLogModel.fetch_all(is_finished=True, user=user_query.username).count()
                session_unfinished_count = SessionLogModel.fetch_all(is_finished=False,
                                                                     user=user_query.username).count()
                strategy_access_count = len(user_query.get_user_strategy_access_queryset())
                strategy_command_count = len(user_query.get_strategy_command_queryset())

                for host_credential in user_query.get_auth_host_credential_queryset():
                    if host_credential.credential.credential_type == "ssh_key":
                        credential_ssh_count += 1
                    else:
                        credential_password_count += 1
                host_id_list = [host.id for host in user_query.get_user_host_queryset_v2()]
                protocol_type = HostModel.PROTOCOL_TYPE[:2]
                host = dict()
                for type in protocol_type:
                    host[type[0]] = HostModel.fetch_all(protocol_type=type[0], id__in=host_id_list).count()
            else:
                host_count = HostModel.fetch_all().count()
                session_finished_count = SessionLogModel.fetch_all(is_finished=True).count()
                session_unfinished_count = SessionLogModel.fetch_all(is_finished=False).count()
                strategy_access_count = StrategyAccessModel.fetch_all().count()
                strategy_command_count = StrategyCommandModel.fetch_all().count()
                credential_password_count = CredentialModel.fetch_all(
                    credential_type=CredentialModel.CREDENTIAL_PASSWORD).count()
                credential_ssh_count = CredentialModel.fetch_all(
                    credential_type=CredentialModel.CREDENTIAL_SSH_KEY).count()

                protocol_type = HostModel.PROTOCOL_TYPE[:2]
                host = dict()
                for type in protocol_type:
                    host[type[0]] = HostModel.fetch_all(protocol_type=type[0]).count()

        end_data = {
            "resource": [
                {"item": "????????????", "count": host_count},
                {"item": "?????????", "count": database_count}
            ],
            "strategy": [
                {"item": "????????????", "count": strategy_access_count},
                {"item": "????????????", "count": strategy_command_count}
            ],
            "session": [
                {"item": "????????????", "count": session_unfinished_count},
                {"item": "????????????", "count": session_finished_count}
            ],
            "credential": [
                {"item": "????????????", "count": credential_password_count},
                {"item": "SSH??????", "count": credential_ssh_count}
            ]
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))


class TestView(View):
    def get(self, request):
        from bastion.utils.iam import Permission
        res = Permission().allowed_visit_host_resources("admin")
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, res))


class AuthenticationView(View):
    def get(self, request):
        action_id = request.GET.get("action_id")
        if not action_id:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="?????????????????????ID"))
        token = request.COOKIES.get("bk_token")
        esb_obj = EsbApi(token)
        res_data = esb_obj.get_user_info()
        username = res_data.get("username")
        try:
            res = Permission().allowed_action(username, action_id)
        except Exception as e:
            print(e)
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="????????????????????????ID"))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, res))
