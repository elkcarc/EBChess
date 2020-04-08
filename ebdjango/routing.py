from channels.routing import ProtocolTypeRouter , URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from main.consumers import MainConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^active/(?P<active_slug>[\w.@+-]+)/$", MainConsumer),
                    url(r"^game/(?P<game_slug>[\w.@+-]+)/$", MainConsumer),
                ]
            )
        )
    )
})