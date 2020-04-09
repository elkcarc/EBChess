from channels.routing import ProtocolTypeRouter , URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import OriginValidator
from main.consumers import ChessBoardConsumer

application = ProtocolTypeRouter({
    'websocket':  AuthMiddlewareStack(
        URLRouter(
            [
                url(r"^active/(?P<active_slug>[\w.@+-]+)/$", ChessBoardConsumer),
                url(r"^game/(?P<game_slug>[\w.@+-]+)/$", ChessBoardConsumer),
            ]
        )
    )
})
