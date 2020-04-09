import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from .models import Game, Challenge, Active, Ai
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChessBoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['url_route']['kwargs'])
        if 'game_slug' in self.scope['url_route']['kwargs']:
            gametype = "game"
            board_id = self.scope['url_route']['kwargs']['game_slug']
            board_obj = await self.get_game(board_id)
        else:
            gametype = "active"
            board_id = self.scope['url_route']['kwargs']['active_slug']
            board_obj = await self.get_active(board_id)  
        
        self.room_name = board_id
        self.room_group_name = gametype

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("Received message:")
        gameupdate_json = json.loads(text_data)
        if text_data is not None:
            print(gameupdate_json)
            if 'game_slug' in self.scope['url_route']['kwargs']:
                gametype = "game"
                board_id = self.scope['url_route']['kwargs']['game_slug']
                board_obj = await self.get_game(board_id)
                board_obj.game_fen = gameupdate_json["fen"]
                board_obj.game_content = gameupdate_json["pgn"]
            else:
                gametype = "active"
                board_id = self.scope['url_route']['kwargs']['active_slug']
                board_obj = await self.get_active(board_id)
                board_obj.game_fen = gameupdate_json["fen"]
                board_obj.game_content = gameupdate_json["pgn"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'move_approval_message',
                    'fen': board_obj.game_fen,
                    'pgn': board_obj.game_content,
                    'movesource': gameupdate_json["movesource"],
                    'movetarget': gameupdate_json["movetarget"],
                }   
            )
            if 'status' in gameupdate_json:
                if "Game" in gameupdate_json["status"]:
                    self.disconnect()

    # Receive message from room group
    async def move_approval_message(self, event):
        # Send message to WebSocket
        print("Sending move approval...")
        print(event)
        await self.send(json.dumps(event))

    async def disconnect(self, close_code):
        # Leave room group
        print("Disconnecting")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_game(self, gid):
        for g in Game.objects.all():
            if str(g.pk) == str(gid):
                #print("found game with game_id = ", gid)
                return g

    @database_sync_to_async
    def get_active(self, aid):
        for a in Active.objects.all():
            if str(a.pk) == str(aid):
                #print("found active with active_id = ", aid)
                return a


