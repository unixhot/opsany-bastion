from django import forms

from bastion.models import HostModel, CredentialModel, HostCredentialRelationshipModel
from bastion.utils.constants import IP_PATTERN


class LinkCheckForm(forms.Form):
    host_id = forms.IntegerField(required=True, error_messages={
        "required": "请选择一台主机"
    })
    credential_id = forms.IntegerField(required=True, error_messages={
        "required": "请选择您的登陆凭证"
    })
    password = forms.CharField(required=False)
    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    font_size = forms.IntegerField(required=False)

    def get_query(self, model, filter):
        try:
            query = model.fetch_one(**filter)
            return True, query
        except:
            return False, None

    def clean_host_id(self):
        host_id = self.cleaned_data.get("host_id")
        status, _ = self.get_query(HostModel, {"id": host_id})
        if not status:
            self.add_error("host_id", "请选择正确的主机")
        return host_id

    def clean_credential_id(self):
        host_id = self.cleaned_data.get("host_id")
        credential_id = self.cleaned_data.get("credential_id")
        status, credential_object = self.get_query(CredentialModel, {"id": credential_id})
        if not status:
            self.add_error("credential_id", "请选择正确的凭证")
        if credential_object.credential_group:
            credential_object_group_id = credential_object.credential_group.id
            if not HostCredentialRelationshipModel.fetch_one(host_id=host_id, credential=credential_object) and not \
                    HostCredentialRelationshipModel.fetch_one(host_id=host_id, credential_group=credential_object_group_id):
                self.add_error("credential_id", "请选择该主机被授权的凭证")
        return credential_id

    def clean_password(self):
        credential_id = self.cleaned_data.get("credential_id")
        password = self.cleaned_data.get("password", "")
        status, credential_object = self.get_query(CredentialModel, {"id": credential_id})
        if credential_object and credential_object.login_type == CredentialModel.LOGIN_HAND:
            if not password:
                self.add_error("password", "当前凭证为手动登陆，请输入您的密码或Passphrase")
        return password


class LinkCheckV2Form(forms.Form):
    host_id = forms.IntegerField(required=True, error_messages={
        "required": "请选择一台主机"
    })
    credential_host_id = forms.IntegerField(required=True, error_messages={
        "required": "请选择您的登陆资源凭证"
    })
    password = forms.CharField(required=False)
    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    font_size = forms.IntegerField(required=False)

    def get_query(self, model, filter):
        try:
            query = model.fetch_one(**filter)
            return True, query
        except:
            return False, None

    def clean_host_id(self):
        host_id = self.cleaned_data.get("host_id")
        status, _ = self.get_query(HostModel, {"id": host_id})
        if not status:
            self.add_error("host_id", "请选择正确的主机")
        return host_id

    def clean_credential_host_id(self):
        host_id = self.cleaned_data.get("host_id")
        credential_host_id = self.cleaned_data.get("credential_host_id")
        status, credential_host_object = self.get_query(HostCredentialRelationshipModel, {"id": credential_host_id})
        if not status:
            self.add_error("credential_host_id", "请选择正确的资源凭证")
        if credential_host_object.credential_group:
            if credential_host_object.host.id != host_id:
                self.add_error("credential_host_id", "请选择该主机被授权的资源凭证")
        return credential_host_id

    def clean_password(self):
        credential_host_id = self.cleaned_data.get("credential_host_id")
        password = self.cleaned_data.get("password", "")
        status, credential_host_object = self.get_query(HostCredentialRelationshipModel, {"id": credential_host_id})
        if credential_host_object and credential_host_object.credential.login_type == CredentialModel.LOGIN_HAND:
            if not password:
                self.add_error("password", "当前凭证为手动登陆，请输入您的密码或Passphrase")
        return password


class GetCacheTokenForm(forms.Form):
    ip = forms.CharField(required=True, error_messages={
        "required": "必须输入IP地址"
    })
    name = forms.CharField(required=True, error_messages={
        "required": "必须输入主机名称"
    })
    ssh_port = forms.IntegerField(required=True, error_messages={
        "required": "必须输入端口"
    })
    system_type = forms.CharField(required=True, error_messages={
        "required": "必须输入系统类型"
    })
    username = forms.CharField(required=False)
    ssh_key_id = forms.IntegerField(required=False)
    password = forms.CharField(required=False)

    def clean_ip(self):
        ip = self.cleaned_data.get("ip")
        if not IP_PATTERN.match(ip):
            self.add_error("ip", "请填写正确的IP地址")
        return ip

    def clean_system_type(self):
        system_type = self.cleaned_data.get("system_type", "").strip()
        if system_type.lower() == "linux":
            return "Linux"
        elif system_type.lower() == "windows":
            return "Windows"
        else:
            self.add_error("system_type", "请填写正确的系统类型")

    def clean_password(self):
        ssh_key_id = self.cleaned_data.get("ssh_key_id", "")
        password = self.cleaned_data.get("password", "")
        username = self.cleaned_data.get("username", "")
        if not password and not ssh_key_id:
            self.add_error("password", "登陆密码或秘钥不能同时为空")
        if not ssh_key_id and not username:
            self.add_error("password", "当使用密码登陆的时候不能没有登录用户名")
        return password