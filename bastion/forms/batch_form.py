from django import forms

from bastion.models import HostModel, HostGroupModel, NetworkProxyModel
from bastion.utils.constants import IP_PATTERN


class ResourceBaseForm(forms.Form):
    host_name_code = forms.CharField(max_length=200, required=True)
    host_name = forms.CharField(max_length=100, required=True)
    system_type = forms.CharField(max_length=20, required=True)
    protocol_type = forms.CharField(max_length=20, required=True)
    host_address = forms.CharField(max_length=150, required=True)
    resource_from = forms.CharField(max_length=30, required=False)
    port = forms.CharField()
    description = forms.CharField(max_length=3000, required=False)
    network_proxy = forms.Field(required=False)

    def clean_port(self):
        port = self.cleaned_data.get('port', "")
        port = port.strip().split(".")[0]
        if port:
            try:
                if 1 <= int(port) <= 65535:
                    return port
                self.add_error('port', '请指定有效范围内的端口')
            except:
                self.add_error('port', '必须指定有效端口')
        self.add_error('port', '该字段必填')

    def clean_host_name_code(self):
        host_name_code = self.cleaned_data.get('host_name_code', "")
        host_name_code = host_name_code.strip()
        if HostModel.fetch_one(host_name_code=host_name_code):
            self.add_error('host_name_code', '唯一标识重复')
        return host_name_code

    def clean_host_address(self):
        host_address = self.cleaned_data.get('host_address', "")
        host_address = host_address.strip()
        if not IP_PATTERN.match(host_address):
            self.add_error('host_address', 'IP地址错误')
        return host_address

    def clean_network_proxy(self):
        network_proxy = self.cleaned_data.get('network_proxy')
        if network_proxy:
            network_proxy_query = NetworkProxyModel.fetch_one(id=network_proxy)
            if not network_proxy_query:
                return self.add_error("network_proxy", "网络代理不存在")
            self.cleaned_data["network_proxy"] = network_proxy_query
            return network_proxy_query
        return network_proxy



# 主机资源表单校验
class ResourceHostForm(ResourceBaseForm):
    resource_type = forms.CharField(max_length=20)
    group = forms.CharField(max_length=20, required=True)

    def clean_resource_type(self):
        resource_type = self.cleaned_data.get('resource_type', "")
        if resource_type != HostModel.RESOURCE_HOST:
            self.add_error('resource_type', '资源类型错误')
        return resource_type

    def clean_group(self):
        group = self.cleaned_data.get('group', "")
        host_group_query = HostGroupModel.fetch_one(id=group, group_type=HostGroupModel.RESOURCE_HOST)
        if not host_group_query:
            self.add_error('group_name', '主机分组不存在')
        return group


# 数据库资源表单验证
class ResourceDatabaseForm(ResourceBaseForm):
    database_type = forms.CharField(max_length=20)
    group_name = forms.CharField(max_length=20, required=True)
    resource_type = forms.CharField(max_length=20)

    def clean_resource_type(self):
        resource_type = self.cleaned_data.get('resource_type', "")
        if resource_type != HostModel.RESOURCE_DATABASE:
            self.add_error('resource_type', '资源类型错误')
        return resource_type
