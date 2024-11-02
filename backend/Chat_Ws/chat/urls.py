from django.urls import path
from .views import RoomApiView, DialogApiView, AddUserRoom, UserViewSet


urlpatterns = [
    path('room/', RoomApiView.as_view()),
    path('dialog/', DialogApiView.as_view()),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('add_users/', AddUserRoom.as_view()),
]