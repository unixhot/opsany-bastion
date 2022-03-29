import json
import uuid
from io import BytesIO

import xlsxwriter
from django.http import JsonResponse, HttpResponse

from bastion.component.common import GetUserInfo
from bastion.component.resource import HostCredential
from bastion.forms import first_error_message
from bastion.forms.batch_form import ResourceHostForm
from bastion.forms.forms import CredentialModelForm
from bastion.models import HostGroupModel, HostModel, CredentialModel, CredentialGroupModel
from bastion.utils.status_code import error, ErrorStatusCode


class CheckImport:
    FIELD_LIST = ["主机名称", "主机唯一标识", "系统类型", "协议类型", "主机地址", "端口", "所属分组", "主机描述"]
    LINUX_EXAMPLE = {
        "主机名称": "Linux演示主机1",
        "主机唯一标识": "linux-node1",
        "系统类型": "Linux",
        "协议类型": "SSH",
        "主机地址": "192.168.56.11",
        "端口": "22",
        "所属分组": "默认分组",
        "主机描述": "这是一台Linux测试机"
    }
    WINDOWS_EXAMPLE = {
        "主机名称": "windows演示主机1",
        "主机唯一标识": "windows-node1",
        "系统类型": "Windows",
        "协议类型": "RDP",
        "主机地址": "192.168.56.12",
        "端口": "3389",
        "所属分组": "默认分组",
        "主机描述": "这是一台Windows测试机"
    }
    COLUMN_WIDTH = {
        "主机名称": 18,
        "主机唯一标识": 18,
        "系统类型": 10,
        "协议类型": 10,
        "主机地址": 15,
        "端口": 10,
        "所属分组": 18,
        "主机描述": 50,
    }

    def __init__(self):
        self.system_type_list = [system[0] for system in HostModel.SYSTEM_TYPE]
        self.protocol_type_list = [protocol[0] for protocol in HostModel.PROTOCOL_TYPE]
        self.group_name_list = [group.name for group in HostGroupModel.fetch_all(group_type="host")]

    def make_excel(self, path=""):
        """
        用于生成下拉菜单
        controller_name: ["xx", "xx", "xx"]
        group_name: ["xx", "xx", "xx"]
        """
        if not self.group_name_list:
            return JsonResponse(error(ErrorStatusCode.CUSTOM_ERROR, custom_message="请先创建主机分组后下载模板并执行导入操作"))
        workbook, x_io = self.get_wrokbook(path)
        workbook = self.add_import_template(workbook)
        workbook.close()
        # 判断返回内容 用于本地测试
        if not path:
            res = HttpResponse()
            res["Content-Type"] = "application/octet-stream"
            res["Content-Disposition"] = 'filename="BastionImportHostTemplate.xlsx'
            res.write(x_io.getvalue())
            return res
        return workbook

    def get_wrokbook(self, path):
        """
        初始化workbook
        """
        if not path:
            path = BytesIO()
        workbook = xlsxwriter.Workbook(path)
        return workbook, path

    def add_import_template(self, workbook):
        # 添加导入模板
        self.add_field(workbook)
        self.add_use_explain(workbook)
        return workbook

    def add_field(self, workbook):
        worksheet = workbook.add_worksheet("导入模板")
        field_format = workbook.add_format({'bold': True, 'font_color': 'red', 'fg_color': "#87CEFA", 'border': 1})
        example_format = workbook.add_format({'bold': False, 'font_color': 'black', 'fg_color': '#A6FFA6', 'border': 1})
        # 设置列宽
        column_count = len(self.FIELD_LIST)
        for column in range(column_count):
            field = self.FIELD_LIST[column]
            worksheet.set_column(column, column, self.COLUMN_WIDTH.get(field))
        # 设置首行字段内容
        for column in range(column_count):
            field = self.FIELD_LIST[column]
            worksheet.write(0, column, field, field_format)
        # 设置Linux主机填写例子
        for field, info in self.LINUX_EXAMPLE.items():
            worksheet.write(1, self.FIELD_LIST.index(field), info, example_format)
        # 设置Windows主机填写例子
        for field, info in self.WINDOWS_EXAMPLE.items():
            worksheet.write(2, self.FIELD_LIST.index(field), info, example_format)
        # 设置后续填写单元格格式
        field_option = {
            "系统类型": self.system_type_list,
            "协议类型": self.protocol_type_list,
            "所属分组": self.group_name_list,
        }
        # 设置后续单元格下拉菜单格式
        for column in range(column_count):
            field = self.FIELD_LIST[column]
            worksheet.data_validation(3, column, 1048575, column,
                                      {"validate": "list", "source": field_option.get(field)}) \
                if field_option.get(field) else ""

    def add_use_explain(self, workbook):
        worksheet = workbook.add_worksheet("使用指南【请勿编辑】")
        for i in range(1, 14):
            worksheet.set_row(i, 16)
        merge_format = workbook.add_format({
            'bold': True,
            'border': 2,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
        })

        top = workbook.add_format({
            'bold': True,
            'border': 2,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'top': 2,
            'left': 0,  # 左边框
            'right': 0,  # 右边框
            'bottom': 0  # 底边框
        })

        left = workbook.add_format({
            'bold': True,
            'border': 2,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'top': 0,
            'left': 2,  # 左边框
            'right': 0,  # 右边框
            'bottom': 0  # 底边框
        })

        cell_format_one = workbook.add_format({'bold': True, 'font_color': 'red', 'fg_color': "#87CEFA", 'border': 1})
        cell_format_two = workbook.add_format(
            {'bold': False, 'font_color': 'black', 'fg_color': '#A6FFA6', 'border': 1})
        cell_format_three = workbook.add_format({'border': 1})
        cell_format_four = workbook.add_format({"align": "center", "valign": "vcenter"})

        worksheet.merge_range("A2:A15", "主机导入", merge_format)
        worksheet.set_column('A:A', 15)
        worksheet.set_column('C:D', 18)
        worksheet.set_column('E:E', 22)
        worksheet.set_column('F:F', 17)
        worksheet.set_column('G:H', 22)
        worksheet.set_column('J:J', 40)

        for i in range(1, 12):
            worksheet.write(1, i, "", top)
            worksheet.write(15, i, "", top)

        for i in range(1, 15):
            worksheet.write(i, 12, "", left)

        # 主机唯一标识
        worksheet.write(3, 2, "不可更改且全表唯一")
        worksheet.write(5, 2, "↑", cell_format_four)
        worksheet.write(7, 2, "主机唯一标识", cell_format_one)
        worksheet.write(8, 2, "linux-node1", cell_format_two)
        worksheet.write(9, 2, "windows-node1", cell_format_two)
        worksheet.write(10, 2, "test-node1", cell_format_three)

        # 系统类型
        worksheet.write(3, 3, "必填选项点击下拉框选择")
        worksheet.write(5, 3, "↑", cell_format_four)
        worksheet.write(7, 3, "系统类型", cell_format_one)
        worksheet.write(8, 3, "Linux", cell_format_two)
        worksheet.write(9, 3, "Windows", cell_format_two)
        worksheet.write(10, 3, "", cell_format_three)

        # 协议类型
        worksheet.write(3, 4, "必填选项点击下拉框选择")
        worksheet.write(5, 4, "↑", cell_format_four)
        worksheet.write(7, 4, "协议类型", cell_format_one)
        worksheet.write(8, 4, "SSH", cell_format_two)
        worksheet.write(9, 4, "RDP", cell_format_two)
        worksheet.write(10, 4, "", cell_format_three)

        # 主机地址
        worksheet.write(3, 5, "必须是有效IP地址")
        worksheet.write(5, 5, "↑", cell_format_four)
        worksheet.write(7, 5, "主机地址", cell_format_one)
        worksheet.write(8, 5, "192.168.56.11", cell_format_two)
        worksheet.write(9, 5, "192.168.56.12", cell_format_two)
        worksheet.write(10, 5, "", cell_format_three)

        # 端口
        worksheet.write(3, 6, "必须是有效端口(1-65535)")
        worksheet.write(5, 6, "↑", cell_format_four)
        worksheet.write(7, 6, "端口", cell_format_one)
        worksheet.write(8, 6, "22", cell_format_two)
        worksheet.write(9, 6, "3389", cell_format_two)
        worksheet.write(10, 6, "", cell_format_three)

        # 所属分组
        worksheet.write(3, 7, "必填选项点击下拉框选择")
        worksheet.write(5, 7, "↑", cell_format_four)
        worksheet.write(7, 7, "所属分组", cell_format_one)
        worksheet.write(8, 7, "默认分组", cell_format_two)
        worksheet.write(9, 7, "默认分组", cell_format_two)
        worksheet.write(10, 7, "", cell_format_three)

        # 说明列
        worksheet.write(7, 8, "→", cell_format_four)
        worksheet.write(8, 8, "→", cell_format_four)
        worksheet.write(9, 8, "→", cell_format_four)
        worksheet.write(10, 8, "→", cell_format_four)
        worksheet.write(7, 9, "第一行是字段名称（不可编辑）")
        worksheet.write(8, 9, "第二行是Linux主机填写例子（不可编辑）")
        worksheet.write(9, 9, "第三行是Windows主机填写例子（不可编辑）")
        worksheet.write(10, 9, "第四行开始为用户需要导入的数据（可编辑）")

        worksheet.write(12, 2, "注意：批量导入暂不支持关联凭据，请手动关联")

    def check_import(self, file, request):
        return


class ImportHostComponent:
    def check_host_data(self, data):
        form = ResourceHostForm(data=data)
        if form.is_valid():
            return True, form
        first_error_message(form)
        return False, None

    def check_credential_data(self, credential=None, credential_list=None, credential_group_list=None,
                              user_name_query=None):
        if not (credential or credential_list or credential_group_list):
            return True, None, None
        # credential 为新建凭据 检查凭据是否可以新建成功
        if credential:
            form_credential = CredentialModelForm(credential)
            if not form_credential.is_valid():
                return False, "credential", first_error_message(form_credential)
            status, message = form_credential.clean_name_unique()
            if not status:
                return False, "credential", message
            form_credential.cleaned_data.update({"user": user_name_query})
            return True, "credential", form_credential.cleaned_data
        # credential_list 为关联已有凭据 检查凭据是否存在
        else:
            dic = {}
            if credential_list:
                credential_id_list = []
                for credential_id in credential_list:
                    credential_query = CredentialModel.fetch_one(id=credential_id)
                    if credential_query:
                        credential_id_list.append(credential_query.id)
                if credential_id_list:
                    dic["credential_list"] = credential_id_list
            if credential_group_list:
                credential_group_id_list = []
                for credential_group_id in credential_group_list:
                    credential_group_query = CredentialGroupModel.fetch_one(id=credential_group_id)
                    if credential_group_query:
                        credential_group_id_list.append(credential_group_query)
                if credential_group_id_list:
                    dic["credential_group_list"] = credential_group_id_list
            if dic:
                return True, "credential_group_list", dic
            else:
                return False, "选择的凭据或凭据分组不存在", {}

    def import_data(self, request):
        user_name_query = GetUserInfo().get_user_info(request)
        if not user_name_query:
            return JsonResponse(error(ErrorStatusCode.CUSTOM_ERROR, custom_message="用户不存在"))
        data = json.loads(request.body)
        data_list = data.get("data_list")
        credential = data.get("credential")
        credential_list = data.get("credential_list")
        credential_group_list = data.get("credential_group_list")
        status, credential_type, credential_data = self.check_credential_data(credential, credential_list,
                                                                              credential_group_list, user_name_query)
        if not status:
            return JsonResponse(error(ErrorStatusCode.HANDLE_ERROR, custom_message=data))
        success_list = []
        error_count = 0
        for data in data_list:
            status, query = self._import_data(data, user_name_query)
            if status:
                success_list.append(query.id)
            else:
                error_count += 1
        if not success_list:
            return JsonResponse(error(ErrorStatusCode.CUSTOM_ERROR, custom_message="未发现有效数据，请检查您的数据内容"))

        if credential_type == "credential":
            credential_query = CredentialModel.create(**credential_data)
            HostCredential()._create_host_credential({"credential": credential_query.id, "host_list": success_list})
        # if credential_type == "credential_list":
        #     for credential_id in credential_data:
        #         HostCredential()._create_host_credential({"credential": credential_id, "host_list": success_list})
        if credential_type == "credential_group_list":
            credential_list = credential_data.get("credential_list", [])
            credential_group_list = credential_data.get("credential_group_list", [])
            if credential_list:
                # for credential_id in credential_list:
                #     HostCredential()._create_host_credential(
                #         {"credential": credential_id, "host_list": success_list})
                for host in success_list:
                    HostCredential()._create_host_credential({"host": host, "credential_list": credential_list})
            if credential_group_list:
                # for credential_group_id in credential_group_list:
                #     HostCredential()._create_host_credential(
                #         {"credential_group": credential_group_id, "host_list": success_list})
                for host in success_list:
                    HostCredential()._create_host_credential({"host": host, "credential_group": credential_group_list})

        message = "成功导入{}条数据".format(str(len(success_list)))
        if error_count:
            message += "，失败{error_count}条".format(error_count=error_count)
        return JsonResponse({'code': 200, 'successcode': 20004, 'message': message})

    def _import_data(self, data, user_name_query=None):
        if isinstance(data, dict):
            data["resource_from"] = "batch_cmdb"
            data["resource_type"] = HostModel.RESOURCE_HOST
        status, form = self.check_host_data(data)
        if status:
            host_query = HostModel.create(**{
                "host_name_code": form.cleaned_data["host_name_code"],
                "host_name": form.cleaned_data["host_name"],
                "system_type": form.cleaned_data["system_type"],
                "protocol_type": form.cleaned_data["protocol_type"],
                "host_address": form.cleaned_data["host_address"],
                "resource_from": form.cleaned_data["resource_from"],
                "network_proxy": form.cleaned_data["network_proxy"],
                "port": form.cleaned_data["port"],
                "description": form.cleaned_data["description"],
                "group_id": form.cleaned_data["group"],
                "user": user_name_query
            })
            return True, host_query
        return False, None
