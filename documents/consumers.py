import json
from channels.generic.websocket import AsyncWebsocketConsumer
from documents.models import Notification
import asyncio

# Dictionary to track connected users per document
connected_users = {}

class DocConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection."""
        self.document_id = self.scope['url_route']['kwargs']['document_id']
        self.room_group_name = f"doc_{self.document_id}"
        self.username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
        self.is_editing = False
        self.editing_reset_task = None
        # Initialize user tracking for this document
        if self.document_id not in connected_users:
            connected_users[self.document_id] = set()

        # Add the user to the connected users list
        connected_users[self.document_id].add(self.username)

        # Join the WebSocket group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Broadcast updated user list to all clients
        await self.send_connected_users()

        # Notify all users in the document room
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": "send_notification",
                "message": f"{self.username} has joined the document!",
            }
        )

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if self.document_id in connected_users:
            connected_users[self.document_id].discard(self.username)  # Remove the user safely

            # If no users are left in the document, remove the entry
            if not connected_users[self.document_id]:
                del connected_users[self.document_id]

        # Notify other users about the disconnection
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": "send_notification",
                "message": f"{self.username} has left the document!",
            }
        )

        # Leave the WebSocket group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Broadcast updated user list
        await self.send_connected_users()

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            text_data_json = json.loads(text_data)
            changes = text_data_json.get("changes")
            cursor_position = text_data_json.get("cursor_position")
            action = text_data_json.get("action")

            # If a user requests the connected users list
            if action == "get_connected_users":
                await self.send_connected_users()
                return

            # Broadcast document updates
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type": "doc_update",
                    "changes": changes,
                    "cursor_position": cursor_position,
                    "sender_channel": self.channel_name  # Sender's WebSocket ID
                }
            )

            # Notify users that someone is editing
            if not self.is_editing:
                self.is_editing = True
                await self.channel_layer.group_send(
                    self.room_group_name, 
                    {
                        "type": "send_notification",
                        "message": f"{self.username} is editing!",
                    }
                )
            # Reset editing flag after 2 seconds of inactivity
            if self.editing_reset_task:
                self.editing_reset_task.cancel()

            self.editing_reset_task = asyncio.create_task(self.reset_editing_flag())

            # Send cursor position update back to the sender
            if cursor_position is not None:
                await self.send(text_data=json.dumps({"cursor_position": cursor_position}))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format"}))

    async def doc_update(self, event):
        """Send document updates to all WebSocket clients except the sender."""
        changes = event.get("changes")
        cursor_position = event.get("cursor_position")
        sender_channel = event.get("sender_channel")

        # Send update to all except the sender
        if self.channel_name != sender_channel:
            await self.send(text_data=json.dumps({
                "changes": changes,
                "cursor_position": cursor_position
            }))

    async def send_notification(self, event):
        """Send real-time notifications to clients."""
        text_data=json.dumps({"notification": event["message"]})
        print(text_data)
        
        await self.send(text_data=json.dumps({"notification": event["message"]}))

    async def send_connected_users(self):
        """Broadcast the list of connected users to all clients in the document room."""
        user_list = list(connected_users.get(self.document_id, []))

        # Send user list update to all group members
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_list_update",
                "users": user_list
            }
        )

    async def user_list_update(self, event):
        """Send the updated list of connected users to the WebSocket client."""
        await self.send(text_data=json.dumps({"connected_users": event["users"]}))
   
    async def reset_editing_flag(self):
        try:
            await asyncio.sleep(2)  # Wait for 2 seconds of inactivity
            self.is_editing = False
        except asyncio.CancelledError:
            pass  # Ignore cancelled tasks (when typing continues)