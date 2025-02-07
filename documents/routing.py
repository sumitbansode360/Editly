from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/doc/edit/(?P<document_id>[a-zA-Z0-9_-]+)/$', consumers.DocConsumer.as_asgi()),
]
