import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print("✅ WebSocket Connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("❌ WebSocket Disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"

        print(f"📩 Received Message: {username}: {message}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username  # Include sender name
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        print(f"📤 Sending Message: {username}: {message}")

        await self.send(text_data=json.dumps({"message": message, "username": username}))
