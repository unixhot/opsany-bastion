import json

from django.http import JsonResponse
from django.views import View

from bastion.component.batch_operation_component import CheckImport, ImportHostComponent
from bastion.utils.status_code import error, ErrorStatusCode


class BatchView(View):
    def get(self, request):
        return CheckImport().make_excel()

    def post(self, request):
        """
        excel导入，检查字数据是否可用，字段是否不合规
        """
        try:
            import_type = json.loads(request.body).get("import_type")
        except Exception as e:
            import_type = request.POST.get("import_type")
        if import_type == "excel":
            file = request.FILES.get("file")
            return CheckImport().check_import(file, request)
        elif import_type == "cmdb":
            return ImportHostComponent().import_data(request)
        else:
            return JsonResponse(error(ErrorStatusCode.PARAMS_ERROR))
