from django.views import View

from bastion.component.network_proxy import NetworkProxy, NetworkProxyResource


class NetworkProxyView(View):
    def get(self, request):
        return NetworkProxy().get_network_proxy(request)

    def post(self, request):
        return NetworkProxy().create_network_proxy(request)

    def put(self, request):
        return NetworkProxy().update_network_proxy(request)

    def delete(self, request):
        return NetworkProxy().delete_network_proxy(request)


class NetworkProxyResourceView(View):
    def get(self, request):
        return NetworkProxyResource().get_network_proxy_resource(request)

    def post(self, request):
        return NetworkProxyResource().create_network_proxy_resource(request)

    def delete(self, request):
        return NetworkProxyResource().delete_network_proxy_resource(request)