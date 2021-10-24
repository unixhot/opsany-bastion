from django.views import View

from bastion.component.core import LinkCheckComponent, HostFileComponent
from bastion.utils.decorator import user_sync


class LinkCheckView(View):
    def get(self, request):
        return LinkCheckComponent().get_token_info(request)

    def post(self, request):
        return LinkCheckComponent().link_check(request)


class LinuxFileView(View):
    def get(self, request):
        return HostFileComponent().get_linux_file(request)

    def post(self, request):
        return HostFileComponent().upload_linux_file(request)

    def delete(self, request):
        return HostFileComponent().delete_linux_file(request)


class WindowsFileView(View):
    def get(self, request):
        return HostFileComponent().get_windows_file(request)

    def post(self, request):
        return HostFileComponent().upload_windows_file(request)

    def delete(self, request):
        return HostFileComponent().delete_windows_file(request)


class LinkCheckV2View(View):
    def get(self, request):
        return LinkCheckComponent().get_token_info(request)

    def post(self, request):
        return LinkCheckComponent().link_check_v2(request)


class GetCacheTokenView(View):
    def post(self, request):
        return LinkCheckComponent().get_cache_token(request)
