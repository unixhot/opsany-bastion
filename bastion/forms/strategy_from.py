import logging
from django import forms

from bastion.models import UserInfo, UserGroupModel, CredentialModel, CredentialGroupModel, CommandGroupModel, \
    CommandModel
from bastion.utils.constants import IP_PATTERN, IP_LIMIT
from bastion.forms import first_error_message

app_logging = logging.getLogger("app")


class NameForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, error_messages={
        "max_length": "名称最大长度不能超过50个字符",
        "required": "名称不能为空"
    })


class IdForm(forms.Form):
    id = forms.IntegerField(required=False)


class BaseCredentialForm(forms.Form):
    password_credential = forms.Field(required=False)
    ssh_credential = forms.Field(required=False)
    credential_group = forms.Field(required=False)

    def list_param_clean(self, model, params, credential_type=""):
        if params:
            try:
                for param in params:
                    query = model.fetch_one(id=param)
                    if not query:
                        return False, ""
                    if credential_type:
                        if query.credential_type != credential_type:
                            return False, "请选择同一类型的凭据"
                return True, ""
            except Exception as e:
                app_logging.error("[ERROR] BaseCredentialForm clean error: {}, param: {}".format(
                    str(e), str(params)
                ))
                return False, ""
        return None, ""

    def clean_password_credential(self):
        password_credential = self.cleaned_data.get("password_credential", [])
        if password_credential:
            status, message = self.list_param_clean(CredentialModel, password_credential,
                                                    CredentialModel.CREDENTIAL_PASSWORD)
            if status is not None:
                if not status:
                    self.add_error("password_credential", "请选择正确的密码凭证" if not message else message)
        return password_credential

    def clean_ssh_credential(self):
        ssh_credential = self.cleaned_data.get("ssh_credential", [])
        if ssh_credential:
            status, message = self.list_param_clean(CredentialModel, ssh_credential, CredentialModel.CREDENTIAL_SSH_KEY)
            if status is not None:
                if not status:
                    self.add_error("ssh_credential", "请选择正确的SSH凭证" if not message else message)
        return ssh_credential

    def clean_credential_group(self):
        password_credential = self.cleaned_data.get("password_credential", [])
        ssh_credential = self.cleaned_data.get("ssh_credential", [])
        credential_group = self.cleaned_data.get("credential_group", [])
        if not password_credential and not ssh_credential and not credential_group:
            self.add_error("credential_group", "请选择关联的凭证/凭证组")
        if credential_group:
            status, message = self.list_param_clean(CredentialGroupModel, credential_group)
            if status is not None:
                if not status:
                    self.add_error("credential_group", "请选择正确的凭证分组")
        return credential_group


class BaseStrategyUserForm(forms.Form):
    user = forms.Field(required=False)
    user_group = forms.Field(required=False)

    def clean_user(self):
        user = self.cleaned_data.get("user")
        if user:
            try:
                for _user in user:
                    if not UserInfo.fetch_one(id=_user):
                        self.add_error("user", "请选择正确的用户")
            except Exception as e:
                app_logging.error("[ERROR] BaseStrategyUserForm clean error: {}, param: {}".format(
                    str(e), str(user)
                ))
                self.add_error("user", "请选择正确的用户")
        return user

    def clean_user_group(self):
        user = self.cleaned_data.get("user")
        user_group = self.cleaned_data.get("user_group")
        if not user and not user_group:
            self.add_error("user_group", "请选择关联的用户/用户组")
        if user_group:
            try:
                for group in user_group:
                    if not UserGroupModel.fetch_one(id=group):
                        self.add_error("user_group", "请选择正确的用户组")
            except Exception as e:
                app_logging.error("[ERROR] BaseStrategyUserForm clean error: {}, param: {}".format(
                    str(e), str(user_group)
                ))
                self.add_error("user_group", "请选择正确的用户组")
        return user_group


class BaseAccessStrategyForm(NameForm, IdForm):
    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)
    file_upload = forms.BooleanField(required=False)
    file_download = forms.BooleanField(required=False)
    file_manager = forms.BooleanField(required=False)
    copy_tool = forms.BooleanField(required=False)
    login_time_limit = forms.Field(required=False)
    ip_limit = forms.IntegerField(required=True, error_messages={
        "required": "IP限制是必填的"
    })
    limit_list = forms.Field(required=False)

    def clean_login_time_limit(self):
        login_time_limit = self.cleaned_data.get("login_time_limit", [])
        if login_time_limit:
            try:
                have_week = []
                for _login_time_limit in login_time_limit:
                    have_day = []
                    if _login_time_limit.get("week") not in [1, 2, 3, 4, 5, 6, 7]:
                        self.add_error("login_time_limit", "请于周一至周日中选择正确的某天")
                    if _login_time_limit.get("time"):
                        for _time in _login_time_limit.get("time"):
                            if _time > 23 or _time < 0:
                                self.add_error("login_time_limit", "请选择正确的时段")
                            else:
                                if _time not in have_day:
                                    have_day.append(_time)
                    if _login_time_limit.get("week") not in have_week:
                        have_week.append(_login_time_limit.get("week"))
                    else:
                        self.add_error("login_time_limit", "访问限制中不能出现每周的同一天")
                    if len(list(set(have_day))) != len(_login_time_limit.get("time")):
                        self.add_error("login_time_limit", "请勿在某一天中选择重复的时间")
            except Exception as e:
                app_logging.error("[ERROR] BaseAccessStrategyForm clean error: {}, param: {}".format(
                    str(e), str(login_time_limit)
                ))
                self.add_error("login_time_limit", "参数错误")
        return login_time_limit

    def clean_ip_limit(self):
        ip_limit = self.cleaned_data.get("ip_limit", [])
        if ip_limit not in IP_LIMIT:
            self.add_error("ip_limit", "IP限制类型不存在，请确认您的数据内容")
        return ip_limit

    def clean_limit_list(self):
        ip_limit = self.cleaned_data.get("ip_limit")
        limit_list = self.cleaned_data.get("limit_list", [])
        if ip_limit != 1:
            if not limit_list:
                self.add_error("limit_list", "当IP限制类型不为无的时候，限制列表不能为空")
            for ip in limit_list:
                if not IP_PATTERN.match(ip):
                    self.add_error("limit_list", "请填写正确的IP地址")
        return limit_list


class AccessStrategyForm(forms.Form):
    strategy = forms.Field(required=True, error_messages={
        "required": "访问策略是必填的"
    })
    user = forms.Field(required=True, error_messages={
        "required": "访问策略必须要关联用户"
    })
    credential = forms.Field(required=True, error_messages={
        "required": "访问策略必须要关联凭证"
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

    def clean_credential(self):
        credential = self.cleaned_data["credential"]
        form = BaseCredentialForm(credential)
        if not form.is_valid():
            self.add_error("credential", first_error_message(form))
        return credential


class BaseCommandStrategyForm(NameForm, IdForm):
    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)
    login_time_limit = forms.Field(required=False)

    def clean_login_time_limit(self):
        login_time_limit = self.cleaned_data.get("login_time_limit", [])
        if login_time_limit:
            try:
                have_week = []
                for _login_time_limit in login_time_limit:
                    have_day = []
                    if _login_time_limit.get("week") not in [1, 2, 3, 4, 5, 6, 7]:
                        self.add_error("login_time_limit", "请于周一至周日中选择正确的某天")
                    if _login_time_limit.get("time"):
                        for _time in _login_time_limit.get("time"):
                            if _time > 23 or _time < 0:
                                self.add_error("login_time_limit", "请选择正确的时段")
                            else:
                                if _time not in have_day:
                                    have_day.append(_time)
                    if _login_time_limit.get("week") not in have_week:
                        have_week.append(_login_time_limit.get("week"))
                    else:
                        self.add_error("login_time_limit", "访问限制中不能出现每周的同一天")
                    if len(list(set(have_day))) != len(_login_time_limit.get("time")):
                        self.add_error("login_time_limit", "请勿在某一天中选择重复的时间")
            except Exception as e:
                app_logging.error("[ERROR] BaseCommandStrategyForm clean error: {}, param: {}".format(
                    str(e), str(login_time_limit)
                ))
                self.add_error("login_time_limit", "参数错误")
        return login_time_limit


class BaseStrategyCommandForm(forms.Form):
    command = forms.Field(required=False)
    command_group = forms.Field(required=False)

    def clean_command(self):
        command = self.cleaned_data.get("command")
        if command:
            try:
                for _command in command:
                    if not CommandModel.fetch_one(id=_command):
                        self.add_error("command", "请选择正确的命令")
            except Exception as e:
                app_logging.error("[ERROR] BaseStrategyCommandForm clean error: {}, param: {}".format(
                    str(e), str(command)
                ))
                self.add_error("command", "请选择正确的命令")
        return command

    def clean_command_group(self):
        command = self.cleaned_data.get("command")
        command_group = self.cleaned_data.get("command_group")
        if not command and not command_group:
            self.add_error("command_group", "请选择关联的命令/命令组")
        if command_group:
            try:
                for group in command_group:
                    if not CommandGroupModel.fetch_one(id=group):
                        self.add_error("command_group", "请选择正确的命令组")
            except Exception as e:
                app_logging.error("[ERROR] BaseStrategyCommandForm clean error: {}, param: {}".format(
                    str(e), str(command_group)
                ))
                self.add_error("command_group", "请选择正确的命令组")
        return command_group


class CommandStrategyForm(AccessStrategyForm):
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

    def clean_credential(self):
        credential = self.cleaned_data["credential"]
        form = BaseCredentialForm(credential)
        if not form.is_valid():
            self.add_error("credential", first_error_message(form))
        return credential