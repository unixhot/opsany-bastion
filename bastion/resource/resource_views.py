from django.views import View

from bastion.component.resource import Host, HostGroup, HostCredential, UserGroup, User, AuthHost, AuthResource
from bastion.utils.decorator import user_sync


class HostGroupView(View):
    def get(self, request, **kwargs):
        return HostGroup().get_host_group(request, **kwargs)

    def post(self, request, **kwargs):
        return HostGroup().create_host_group(request, **kwargs)

    def put(self, request, **kwargs):
        return HostGroup().update_host_group(request, **kwargs)

    def delete(self, request, **kwargs):
        return HostGroup().delete_host_group(request, **kwargs)


class HostGroupConsoleView(View):
    @user_sync
    def get(self, request):
        return HostGroup().get_host_group_console(request)


class HostView(View):
    def get(self, request, **kwargs):
        return Host().get_host(request, **kwargs)

    def post(self, request, **kwargs):
        return Host().create_host(request, **kwargs)

    def put(self, request, **kwargs):
        return Host().update_host(request, **kwargs)

    def delete(self, request, **kwargs):
        return Host().delete_host(request, **kwargs)


class AuthHostView(View):
    def get(self, request):
        return AuthHost().get_auth_host(request)

class AuthResourceView(View):
    def get(self, request, **kwargs):
        return AuthResource().get_auth_resource(request, **kwargs)


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
