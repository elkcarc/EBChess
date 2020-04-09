from django.urls import re_path

from .consumers import consumers

websocket_urlpatterns = [
    re_path(r"^game/(?P<game_slug>[\w.@+-]+)/$", ChessBoardConsumer),
    re_path(r"^active/(?P<active_slug>[\w.@+-]+)/$", ChessBoardConsumer),
]