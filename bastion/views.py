from django.views import View
from django.http import JsonResponse

from bastion.utils.status_code import success, SuccessStatusCode, error, ErrorStatusCode
from bastion.utils.iam import Permission
from bastion.utils.esb_api import EsbApi
from bastion.models import HostModel, CredentialModel, StrategyAccessModel, StrategyCommandModel, SessionLogModel


class GetInfoForWorkbenchView(View):
    def get(self, request):
        end_data = {
            "resource": [
                {"item": "数据库", "count": 0},
                {"item": "数据库", "count": HostModel.fetch_all().count()}
            ],
            "strategy": [
                {"item": "访问策略", "count": StrategyAccessModel.fetch_all().count()},
                {"item": "命令策略", "count": StrategyCommandModel.fetch_all().count()}
            ],
            "session": [
                {"item": "在线会话", "count": SessionLogModel.fetch_all(is_finished=False).count()},
                {"item": "历史会话", "count": SessionLogModel.fetch_all(is_finished=True).count()}
            ],
            "credential": [
                {"item": "密码凭证", "count": CredentialModel.fetch_all(
                    login_type=CredentialModel.CREDENTIAL_PASSWORD).count()},
                {"item": "SSH秘钥", "count": CredentialModel.fetch_all(
                    login_type=CredentialModel.CREDENTIAL_SSH_KEY).count()}
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
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="请输入您的动作ID"))
        token = request.COOKIES.get("bk_token")
        esb_obj = EsbApi(token)
        res_data = esb_obj.get_user_info()
        username = res_data.get("username")
        try:
            res = Permission().allowed_action(username, action_id)
        except Exception as e:
            print(e)
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="请输入正确的动作ID"))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, res))
