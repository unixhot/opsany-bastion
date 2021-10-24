from bastion.core.consumers import WebSSH, GuacamoleWebsocket
from django.urls import re_path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

websocket_urlpatterns = [
            re_path(r'^ws/bastion/terminalchannel/$', WebSSH),
            re_path(r'^ws/bastion/guacamole/$', GuacamoleWebsocket),
        ]
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})