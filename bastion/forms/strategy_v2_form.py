import logging
from django import forms

from bastion.models import UserInfo, UserGroupModel, CredentialModel, CredentialGroupModel, CommandGroupModel, \
    CommandModel, StrategyAccessCredentialHostModel, HostCredentialRelationshipModel
from bastion.forms.strategy_from import BaseAccessStrategyForm, BaseStrategyUserForm, BaseStrategyCommandForm, \
    BaseCommandStrategyForm
from bastion.forms import first_error_message

app_logging = logging.getLogger("app")


class NameForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, error_messages={
        "max_length": "名称最大长度不能超过50个字符",
        "required": "名称不能为空"
    })


class IdForm(forms.Form):
    id = forms.IntegerField(required=False)


class BaseCredentialHostForm(forms.Form):
    ssh_credential_host_id = forms.Field(required=False)
    password_credential_host_id = forms.Field(required=False)
    credential_group = forms.Field(required=False)

    def list_param_clean(self, model, params, credential_type=""):
        if params:
            try:
                for param in params:
                    query = model.fetch_one(id=param)
                    if not query:
                        return False, ""
                    if credential_type:
                        if query.credential.credential_type != credential_type:
                            return False, "请选择同一类型的凭据"
                return True, ""
            except Exception as e:
                app_logging.error("[ERROR] BaseCredentialHostForm clean error: {}, param: {}".format(
                    str(e), str(params)
                ))
                return False, ""
        return None, ""

    def clean_password_credential_host_id(self):
        password_credential_host_id = self.cleaned_data.get("password_credential_host_id", [])
        if password_credential_host_id:
            status, message = self.list_param_clean(HostCredentialRelationshipModel, password_credential_host_id,
                                                    CredentialModel.CREDENTIAL_PASSWORD)
            if status is not None:
                if not status:
                    self.add_error("password_credential_host", "请选择正确的密码资源凭证" if not message else message)
        return password_credential_host_id

    def clean_ssh_credential_host_id(self):
        ssh_credential_host_id = self.cleaned_data.get("ssh_credential_host_id", [])
        if ssh_credential_host_id:
            status, message = self.list_param_clean(HostCredentialRelationshipModel, ssh_credential_host_id,
                                                    CredentialModel.CREDENTIAL_SSH_KEY)
            if status is not None:
                if not status:
                    self.add_error("ssh_credential_host", "请选择正确的SSH资源凭证" if not message else message)
        return ssh_credential_host_id

    def clean_credential_group(self):
        password_credential = self.cleaned_data.get("password_credential_host_id", [])
        ssh_credential = self.cleaned_data.get("ssh_credential_host_id", [])
        credential_group = self.cleaned_data.get("credential_group", [])
        if not password_credential and not ssh_credential and not credential_group:
            self.add_error("credential_group", "请选择关联的资源凭证/凭证分组")
        if credential_group:
            status, message = self.list_param_clean(CredentialGroupModel, credential_group)
            if status is not None:
                if not status:
                    self.add_error("credential_group", "请选择正确的凭证分组")
        return credential_group


class AccessStrategyV2Form(forms.Form):
    strategy = forms.Field(required=True, error_messages={
        "required": "访问策略是必填的"
    })
    user = forms.Field(required=True, error_messages={
        "required": "访问策略必须要关联用户"
    })
    credential_host = forms.Field(required=True, error_messages={
        "required": "访问策略必须要关联资源凭证"
    })

    def clean_strategy(self):
        strategy = self.cleaned_data["strategy"]
        form = BaseAccessStrategyForm(strategy)
        if not form.is_valid():
            self.add_error("strategy", first_error_message(form))
        return strategy

    def clean_user(self):
        user = self.cleaned_data["user"]
        form = BaseStrategyUserForm(user)
        if not form.is_valid():
            self.add_error("user", first_error_message(form))
        return user

    def clean_credential_host(self):
        credential_host = self.cleaned_data["credential_host"]
        form = BaseCredentialHostForm(credential_host)
        if not form.is_valid():
            self.add_error("credential_host", first_error_message(form))
        return credential_host


class CommandStrategyV2Form(AccessStrategyV2Form):
    command = forms.Field(required=True, error_messages={
        "required": "访问策略是必填的"
    })

    def clean_command(self):
        command = self.cleaned_data["command"]
        form = BaseStrategyCommandForm(command)
        if not form.is_valid():
            self.add_error("command", first_error_message(form))
        return command

    def clean_strategy(self):
        strategy = self.cleaned_data["strategy"]
        form = BaseCommandStrategyForm(strategy)
        if not form.is_valid():
            self.add_error("strategy", first_error_message(form))
        return strategy

    def clean_user(self):
        user = self.cleaned_data["user"]
        form = BaseStrategyUserForm(user)
        if not form.is_valid():
            self.add_error("user", first_error_message(form))
        return user

    def clean_credential_host(self):
        credential_host = self.cleaned_data["credential_host"]
        form = BaseCredentialHostForm(credential_host)
        if not form.is_valid():
            self.add_error("credential_host", first_error_message(form))
        return credential_host