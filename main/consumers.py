import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Game, Challenge, Active, Ai

class ChatConsumer(AsyncConsumer):
    async def websocker_connect(self, event):
        print ("connected", event)

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)