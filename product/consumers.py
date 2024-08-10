import json

from django.utils.timesince import timesince
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .templatetags.roomextras import initials
from .models import Message, User, Room

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name=self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name=f'chat_{self.room_name}'

        # Join room
        await self.get_room()
        print("from connect: ", self.room)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Receive message from client
        text_data_json = json.loads(text_data)
        print(text_data)
        type = text_data_json["type"]
        message = text_data_json["message"]
        name = text_data_json["name"]
        agent = text_data_json.get("agent", "")

        print("Received: ", type)
        if type == "message":
            #Send message to room
            new_message = await self.create_message(name, message, agent)
            await self.channel_layer.group_send(self.room_group_name,{
                "type":"chat_message",
                "message": message,
                "name": name,
                "agent": agent,
                "initials": initials(name),
                "created_at": ''
            })

    async def chat_message(self, event):
        # Send to websocket
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "message": event["message"],
            "name": event["name"],
            "agent": event["agent"],
            "initials": event["initials"],
            "created_at": event["created_at"]
        }))
    
    @sync_to_async
    def get_room(self):
        self.room = Room.objects.filter(uuid=self.room_name).first()

    @sync_to_async    
    def create_message(self, sent_by, message, agent):
        message = Message.objects.create(body=message, sent_by=sent_by)

        if agent:
            message.created_by=User.objects.get(pk=agent)
            message.save()
        
        self.room = Room.objects.filter(client=self.room_name).first()
        self.room.messages.add(message)

        return message