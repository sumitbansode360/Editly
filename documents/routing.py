from django.urls import path

from documents.consumers import DocConsumer
websocket_urlpatterns = [
    path(r"ws/doc/edit/", DocConsumer.as_asgi()),
]