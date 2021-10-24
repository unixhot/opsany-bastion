from django.views import View

from bastion.component.resource import Host, HostGroup, HostCredential, UserGroup, User, AuthHost
from bastion.utils.decorator import user_sync


class HostGroupView(View):
    def get(self, request):
        return HostGroup().get_host_group(request)

    def post(self, request):
        return HostGroup().create_host_group(request)

    def put(self, request):
        return HostGroup().update_host_group(request)

    def delete(self, request):
        return HostGroup().delete_host_group(request)


class HostGroupConsoleView(View):
    @user_sync
    def get(self, request):
        return HostGroup().get_host_group_console(request)


class HostView(View):
    def get(self, request):
        return Host().get_host(request)

    def post(self, request):
        return Host().create_host(request)

    def put(self, request):
        return Host().update_host(request)

    def delete(self, request):
        return Host().delete_host(request)


class AuthHostView(View):
    def get(self, request):
        return AuthHost().get_auth_host(request)


class HostCredentialView(View):
    def get(self, request):
        return HostCredential().get_host_credential(request)

    def post(self, request):
        return HostCredential().create_host_credential(request)

    def delete(self, request):
        return HostCredential().delete_host_credential(request)


class UserInfoView(View):
    def get(self, request):
        return User().get_user_info(request)


class GroupView(View):
    def get(self, request):
        return UserGroup().get_user_group_info(request)
