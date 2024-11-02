from django.urls import path
from .consumers import RoomConsumer

ws_urlpatterns = [
    path('ws/chat/<int:room_name>/', RoomConsumer.as_asgi())
]