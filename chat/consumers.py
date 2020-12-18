import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Move


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        room = await self.get_room(self.room_name.upper())
        if not room.p1_code and room.p1:
            room.p1_code = self.channel_name
        elif not room.p2_code and room.p2:
            room.p2_code = self.channel_name
        await self.save_room(room)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_room(self, code):
        return Room.objects.get(code=code)

    @database_sync_to_async
    def clear_player(self, room, player):
        if player == 'p1':
            room.p1 = None
            room.p1_uid = None
            room.p1_code = None
            room.p1_ready = False
            room.p2_ready = False
        else:
            room.p2 = None
            room.p2_uid = None
            room.p2_code = None
            room.p1_ready = False
            room.p2_ready = False
        if not (room.p1_code or room.p2_code):
            return self.room.delete(room)
        return self.save_room(room)

    @database_sync_to_async
    def save_room(self, room):
        room.save()

    @database_sync_to_async
    def delete_room(self, room):
        room.delete()

    async def disconnect(self, close_code):
        room = await database_sync_to_async(Room.objects.get)(code=self.room_name.upper())
        if room and room.p1_code == self.channel_name:
            await self.clear_player(room, "p1")
        elif room and room.p2_code == self.channel_name:
            await self.clear_player(room, "p2")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message['message'],
            'user': message['user'],
            'type': message['type']
        }))
