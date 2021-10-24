from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms import ModelForm

from bastion.models import CredentialGroupModel, CredentialModel, HostGroupModel, HostModel, \
    CredentialGroupRelationshipModel, HostCredentialRelationshipModel, CommandGroupModel, CommandModel, \
    CommandGroupRelationshipModel
from bastion.utils.encryption import PasswordEncryption


class CredentialGroupForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, error_messages={
        "max_length": "名称最大长度不能超过100个字符",
        "required": "名称不能为空"
    })
    description = forms.CharField(max_length=2000, required=False, error_messages={
        "max_length": "描述信息最大长度不能超过2000个字符"
    })

    def clean_name_unique(self):
        a = CredentialGroupModel.fetch_one(name=self.cleaned_data.get("name"))
        if a:
            raise ValidationError("已存在")


class BastionModelForm(ModelForm):
    pass


class CredentialGroupModelForm(ModelForm):
    class Meta:
        model = CredentialGroupModel
        fields = "__all__"
        exclude = ["user"]
        error_messages = {
            'name': {'required': "分组名称不能为空", "max_length": "名称最大长度不能超过100个字符"},
            'description': {"max_length": "描述信息最大长度不能超过2000个字符"},
        }

    def clean_name_unique(self):
        if CredentialGroupModel.fetch_one(name=self.cleaned_data.get("name")):
            return False, "凭据分组名称已存在"
        return True, ""


class CredentialModelForm(ModelForm):
    class Meta:
        model = CredentialModel
        fields = "__all__"
        exclude = ["user", "login_password", "ssh_key", "passphrase"]
        error_messages = {
            'name': {"max_length": "凭据名称最大长度不能超过100个字符", 'required': "凭据名称不能为空"},
            'login_type': {"invalid_choice": "登录方式不存在"},
            'credential_type': {"invalid_choice": "凭据类型不存在"},
            'login_name': {"max_length": "登录名最大长度不能超过50个字符"},
            'description': {"max_length": "描述信息最大长度不能超过2000个字符"},
        }

    def clean_name(self):
        login_password = self._encrypt_password(self.data.pop("login_password", None))
        if login_password:
            self.cleaned_data["login_password"] = login_password
        passphrase = self._encrypt_password(self.data.pop("passphrase", None))
        if passphrase:
            self.cleaned_data["passphrase"] = passphrase
        ssh_key = self._check_ssh_key(self.data.pop("ssh_key", None))
        if ssh_key:
            self.cleaned_data["ssh_key"] = ssh_key
        return self.cleaned_data.get("name")

    def _check_ssh_key(self, ssh_key):
        if ssh_key:
            if ssh_key == "******":
                return None
            else:
                return ssh_key
        return None

    def _encrypt_password(self, password):
        if password:
            if password == "******":
                return None
            else:
                return PasswordEncryption().encrypt(password)
        return None

    def in_fields(self):
        filed_list = list(self.data.keys())
        model_fields = ["name", "description", "user"]
        for i in filed_list:
            if i not in model_fields:
                return 0
        return 1

    def clean_name_unique(self):
        if CredentialModel.fetch_one(name=self.cleaned_data.get("name")):
            return False, "凭据名称已存在"
        return True, ""


class HostGroupModelForm(ModelForm):
    class Meta:
        model = HostGroupModel
        fields = "__all__"
        exclude = ["user"]
        error_messages = {
            'name': {'required': "主机分组名称不能为空", "max_length": "主机分组名称最大长度不能超过100个字符"},
            'parent': {"invalid_choice": "上级主机分组不存在"},
            'description': {"max_length": "描述信息最大长度不能超过2000个字符"},
        }

    def clean_name_unique(self):
        if HostGroupModel.fetch_one(name=self.cleaned_data.get("name")):
            return False, "主机分组已存在"
        return True, ""

    def check_delete(self, id):
        child_host_group_query = HostGroupModel.fetch_one(parent_id=id)
        if child_host_group_query:
            return False, "当前分组下有关联分组无法删除"
        host_query = HostModel.fetch_one(group_id=id)
        if host_query:
            return False, "当前分组下有关联主机无法删除"
        return True, ""


class HostModelForm(ModelForm):
    class Meta:
        model = HostModel
        fields = "__all__"
        exclude = ["user"]
        error_messages = {
            'host_name_code': {'required': "主机唯一标识不能为空", "max_length": "主机名称最大长度不能超过200个字符"},
            'host_name': {'required': "主机名称不能为空", "max_length": "主机名称最大长度不能超过100个字符"},
            'system_type': {'required': "系统类型不能为空", "invalid_choice": "系统类型不存在"},
            'protocol_type': {'required': "协议类型不能为空", "invalid_choice": "协议类型不存在"},
            'host_address': {'required': "主机地址不能为空", "max_length": "主机地址最大长度不能超过150个字符"},
            'port': {'required': "主机端口不能为空"},
            'group': {'required': "主机分组不能为空", "invalid_choice": "主机分组不存在"},
            'description': {"max_length": "描述信息最大长度不能超过2000个字符"},
        }

    def clean_host_name_unique(self):
        if HostModel.fetch_one(host_name=self.cleaned_data.get("host_name")):
            return False, "主机已存在"
        return True, ""

    def clean_resource_from(self):
        resource_from = self.cleaned_data.get("resource_from")
        if resource_from:
            if resource_from not in ["hand", "cmdb", "batch_cmdb", "batch_excel"]:
                self.add_error("resource_from", "资源来源不明")
        return resource_from


class GroupCredentialModelForm(ModelForm):
    class Meta:
        model = CredentialGroupRelationshipModel
        fields = "__all__"
        exclude = ["user"]
        error_messages = {
            'credential': {"invalid_choice": "凭据不存在"},
            'credential_group': {"invalid_choice": "凭据分组不存在"},
            NON_FIELD_ERRORS: {'unique_together': "记录已存在"}
        }


class HostCredentialModelForm(ModelForm):
    class Meta:
        model = HostCredentialRelationshipModel
        fields = "__all__"
        exclude = ["user"]
        error_messages = {
            'host': {'required': "主机不能为空", "invalid_choice": "主机不存在"},
            'credential': {'required': "凭据不能为空", "invalid_choice": "凭据不存在"},
            'credential_group': {'required': "分组不能为空", "invalid_choice": "凭据分组不存在"},
            NON_FIELD_ERRORS: {'unique_together': "记录已存在"}
        }


class CommandGroupModelForm(ModelForm):
    class Meta:
        model = CommandGroupModel
        fields = "__all__"
        exclude = ["user"]
        error_messages = {
            'name': {'required': "命令分组名称不能为空"},
            'description': {"max_length": "描述信息最大长度不能超过2000个字符"}
        }

    def clean_name_unique(self):
        if CommandGroupModel.fetch_one(name=self.cleaned_data.get("name")):
            return False, "分组已存在"
        return True, ""


class CommandModelForm(ModelForm):
    class Meta:
        model = CommandModel
        fields = "__all__"
        exclude = ["user"]
        error_messages = {
            'command': {'required': "命令不能为空", "max_length": "命令最大长度不能超过255个字符"},
            'block_type': {'required': "阻断类型不能为空", "max_length": "阻断类型最大长度不能超过255个字符"},
            'block_info': {'required': "阻断提示信息不能为空", "max_length": "阻断提示信息最大长度不能超过255个字符"}
        }

    def clean_block_type(self):
        block_type = self.cleaned_data.get("block_type")
        if self.cleaned_data.get("block_type") not in [1, 2]:
            raise ValidationError("阻断类型不存在")
        return block_type

    def clean_command_unique(self):
        if CommandModel.fetch_one(command=self.cleaned_data.get("command")):
            return False, "分组已存在"
        return True, ""


class GroupCommandModelForm(ModelForm):
    class Meta:
        model = CommandGroupRelationshipModel
        fields = "__all__"
        exclude = ["user"]
        error_messages = {
            'command': {'required': "命令不能为空", "invalid_choice": "命令不存在"},
            'command_group': {'required': "命令分组不能为空", "invalid_choice": "命令分组不存在"},
            NON_FIELD_ERRORS: {'unique_together': "记录已存在"}
        }
