import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from .models import Game, Challenge, Active, Ai
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from datetime import datetime

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
        if gametype == "active":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'init_message',
                    'fen': board_obj.active_fen,
                    'pgn': board_obj.active_content,
                })
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'init_message',
                    'fen': board_obj.game_fen,
                    'pgn': board_obj.game_content,
                })
            
    async def init_message(self, event):
        # Send message to WebSocket
        print("Sending init fen...")
        print(event)
        await self.send(json.dumps(event))

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("Received message:")
        gameupdate_json = json.loads(text_data)
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
            board_obj.active_fen = gameupdate_json["fen"]
            board_obj.active_content = gameupdate_json["pgn"]
        if 'status' in gameupdate_json and gametype == "active":
            if "Game" in gameupdate_json["status"]:
                if gameupdate_json["moveColor"] == "Black":
                    result = "1-0"
                elif gameupdate_json["moveColor"] == "White":
                    result = "0-1"
                if "drawn" in gameupdate_json["status"]:
                    result = "1/2-1/2"
                self.update_active(gameupdate_json)
                activeObj = Active.objects.filter(pk=self.scope['url_route']['kwargs']['active_slug'])
                print(activeObj[0].active_fen)
                new_game_obj = Game(game_event="No Event",
                                    game_site="On-line",
                                    game_published=datetime.now(),
                                    game_round="1",
                                    game_white=activeObj[0].user1,
                                    game_black=activeObj[0].user2,
                                    game_result=result,
                                    game_content=activeObj[0].active_content,
                                    game_fen=activeObj[0].active_fen)
                new_game_obj.save()
                instance = Active.objects.get(active_id=activeObj[0].active_id)
                instance.delete()
                self.disconnect(0)
                return
        elif text_data is not None:
            print(gameupdate_json)         
            if gametype == "game":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'move_approval_message',
                        'fen': board_obj.game_fen,
                        'pgn': board_obj.game_content,
                        'movesource': gameupdate_json["movesource"],
                        'movetarget': gameupdate_json["movetarget"],
                        'promotion': gameupdate_json["promotion"],
                    }   
                )
            if gametype == "active":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'move_approval_message',
                        'fen': board_obj.active_fen,
                        'pgn': board_obj.active_content,
                        'movesource': gameupdate_json["movesource"],
                        'movetarget': gameupdate_json["movetarget"],
                        'promotion': gameupdate_json["promotion"],
                    }   
                )
                self.update_active(gameupdate_json)

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

    def update_active(self, data):
        active = Active.objects.filter(pk=self.scope['url_route']['kwargs']['active_slug'])
        #print(active[0].active_fen)
        active.update(active_content=data["pgn"])
        active.update(active_fen=data["fen"])
        active[0].save()
        #print(active[0].active_fen)
        
