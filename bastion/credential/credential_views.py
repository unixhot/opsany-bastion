from django.views import View

from bastion.component.credential import CredentialGroup, Credential, GroupCredential, SyncUserGroup, CommandGroup, \
    Command, GroupCommand


class CredentialGroupView(View):
    def get(self, request):
        return CredentialGroup().get_credential_group(request)

    def post(self, request):
        return CredentialGroup().create_credential_group(request)

    def put(self, request):
        return CredentialGroup().update_credential_group(request)

    def delete(self, request):
        return CredentialGroup().delete_credential_group(request)


class CredentialView(View):
    def get(self, request):
        return Credential().get_credential(request)

    def post(self, request):
        return Credential().create_credential(request)

    def put(self, request):
        return Credential().update_credential(request)

    def delete(self, request):
        return Credential().delete_credential(request)


class GroupCredentialView(View):
    def get(self, request):
        return GroupCredential().get_group_credential(request)

    def post(self, request):
        return GroupCredential().create_group_credential(request)

    def delete(self, request):
        return GroupCredential().delete_group_credential(request)


class CommandGroupView(View):
    def get(self, request):
        return CommandGroup().get_command_group(request)

    def post(self, request):
        return CommandGroup().create_command_group(request)

    def put(self, request):
        return CommandGroup().update_command_group(request)

    def delete(self, request):
        return CommandGroup().delete_command_group(request)


class CommandView(View):
    def get(self, request):
        return Command().get_command(request)

    def post(self, request):
        return Command().create_command(request)

    def put(self, request):
        return Command().update_command(request)

    def delete(self, request):
        return Command().delete_command(request)


class GroupCommandView(View):
    def post(self, request):
        return GroupCommand().create_group_command_group(request)

    def delete(self, request):
        return GroupCommand().delete_group_command(request)


class SyncUserGroupView(View):
    def get(self, request):
        return SyncUserGroup().sync_user_group(request)
