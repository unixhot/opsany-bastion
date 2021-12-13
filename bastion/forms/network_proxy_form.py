from django.forms import ModelForm

from bastion.models import NetworkProxyModel
from bastion.utils.constants import IP_PATTERN
from bastion.utils.encryption import PasswordEncryption


class NetworkProxyModelForm(ModelForm):
    class Meta:
        model = NetworkProxyModel
        fields = "__all__"
        exclude = ["user", "linux_login_password"]
        error_messages = {
            'name': {'required': "名称不能为空", "max_length": "登录名最大长度不能超过255个字符"},
            'linux_ip': {"max_length": "登录名最大长度不能超过150个字符"},
            'linux_port': {"max_length": "登录名最大长度不能超过22个字符"},
            'linux_login_name': {"max_length": "登录名最大长度不能超过50个字符"},
            # 'linux_login_password': {"max_length": "登录名最大长度不能超过500个字符"},
            'windows_ip': {"max_length": "登录名最大长度不能超过150个字符"},
            'windows_port': {"max_length": "登录名最大长度不能超过22个字符"},
            'description': {"max_length": "登录名最大长度不能超过2000个字符"},
        }

    # def clean(self):
    #     linux_params_count, windows_params_count = 0, 0
    #     linux_ip = self.cleaned_data.get("linux_ip")
    #     linux_port = self.cleaned_data.get("linux_port")
    #     linux_login_name = self.cleaned_data.get("linux_login_name")
    #     linux_login_password = self.data.get("linux_login_password")
    #     windows_ip = self.data.get("windows_ip")
    #     windows_port = self.data.get("windows_port")
    #     if linux_ip: linux_params_count += 1
    #     if linux_port: linux_params_count += 1
    #     if linux_login_name: linux_params_count += 1
    #     if linux_login_password: linux_params_count += 1
    #     if windows_ip: windows_params_count += 1
    #     if windows_port: windows_params_count += 1
    #     if linux_params_count == 4:
    #         if self.check_Chinese(linux_login_name):
    #             self.add_error("linux_login_name", "资源账户不支持中文")
    #         if linux_login_password and linux_login_password != "******":
    #             if len(linux_login_password) > 200:
    #                 self.add_error("name", "密码长度超限")
    #             self.cleaned_data["linux_login_password"] = self._encrypt_password(linux_login_password)
    #     elif linux_params_count == 3 and not linux_login_password:
    #         pass
    #     elif linux_params_count == 0:
    #         if windows_params_count == 0:
    #             self.add_error("name", "至少选择一种代理")
    #     else:
    #         self.add_error("linux_ip", "当选择Linux为代理时请完整输入Linux主机地址、端口、登录名和密码等信息")
    #     if windows_params_count == 1:
    #         self.add_error("windows_ip", "当选择Windows为代理时请完整输入Windows主机地址和端口等信息")
    #     return self.cleaned_data

    def clean(self):
        linux_ip = self.cleaned_data.get("linux_ip")
        linux_port = self.cleaned_data.get("linux_port")
        linux_login_name = self.cleaned_data.get("linux_login_name")
        linux_login_password = self.data.get("linux_login_password")
        windows_ip = self.data.get("windows_ip")
        windows_port = self.data.get("windows_port")
        if all([linux_ip, linux_port, linux_login_name, linux_login_password]):
            if self.check_Chinese(linux_login_name):
                self.add_error("linux_login_name", "用户名不支持中文")
            if linux_login_password and linux_login_password != "******":
                if len(linux_login_password) > 200:
                    self.add_error("name", "密码长度超限")
                self.cleaned_data["linux_login_password"] = self._encrypt_password(linux_login_password)
        elif not linux_ip and not linux_port and not linux_login_name and not linux_login_password:
            pass
        else:
            self.add_error("linux_ip", "当选择Linux为代理时请完整输入Linux主机地址、端口、登录名和密码等信息")
        if all([windows_ip, windows_port]):
            pass
        elif not windows_ip and not windows_port:
            pass
        else:
            self.add_error("windows_ip", "当选择Windows为代理时请完整输入Windows主机地址和端口等信息")
        if not all([linux_ip, linux_port, linux_login_name, linux_login_password]) and not all([windows_ip, windows_port]):
            self.add_error("name", "至少选择一种代理")

        return self.cleaned_data

    def _encrypt_password(self, password):
        return PasswordEncryption().encrypt(password)

    def clean_linux_port(self):
        linux_port = self.data.get("linux_port")
        if linux_port:
            if 1 <= int(linux_port) <= 65535:
                return linux_port
            self.add_error('linux_port', '请指定有效范围内的端口')
        return linux_port


    def clean_windows_port(self):
        windows_port = self.data.get("windows_port")
        if windows_port:
            if 1 <= int(windows_port) <= 65535:
                return windows_port
            self.add_error('windows_port', '请指定有效范围内的端口')
        return windows_port

    def clean_linux_ip(self):
        linux_ip = self.cleaned_data.get('linux_ip', "")
        if linux_ip:
            if not IP_PATTERN.match(linux_ip):
                self.add_error('linux_ip', 'IP地址不合法')
        return linux_ip

    def clean_windows_ip(self):
        windows_ip = self.cleaned_data.get('windows_ip', "")
        if windows_ip:
            if not IP_PATTERN.match(windows_ip):
                self.add_error('windows_ip', 'IP地址不合法')
        return windows_ip

    def check_Chinese(self, word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False
