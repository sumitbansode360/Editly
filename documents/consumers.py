import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class DocConsumer(WebsocketConsumer):
    def connect(self):
        self.document_id = self.scope['url_route']['kwargs']['document_id']
        self.room_group_name = f"doc_{self.document_id}"
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps({"success": "connection done"}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        changes = text_data_json["changes"]

         # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "doc_update", "changes": changes}
        )
    
    def doc_update(self, event):
        changes = event["changes"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"changes": changes}))