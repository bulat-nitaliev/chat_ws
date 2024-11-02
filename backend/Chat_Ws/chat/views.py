from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from rest_framework.response import Response
from chat.models import Room, Chat, User
from chat.serializers import (RoomSerializer, ChatSerializers, ChatPostSerializers,  UserSerializer, UserRegistrationSerializer)
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from chat.serializers import CookieTokenRefreshSerializer, MyTokenObtainPairSerializer
from datetime import timedelta


class UserViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    '''Вьюшка создания пользователя и получения списков пользователей'''
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny,]
    def get_serializer_class(self):
        if self.action == 'create':
           return UserRegistrationSerializer
        return UserSerializer
        


class RoomApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        rooms = Room.objects.filter(Q(creator=request.user) | Q(invited=request.user))
        serializer = RoomSerializer(rooms, many=True)
        return Response({'data': serializer.data})
    
    def post(self,request):
        Room.objects.create(creator=request.user)
        return Response(status=status.HTTP_201_CREATED)


class DialogApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        room = request.GET.get('room')
        chat = Chat.objects.filter(room=room)
        serializer = ChatSerializers(chat, many=True)

        return Response({'data': serializer.data})

    def post(self, request):
        dialog = ChatPostSerializers(data=request.data)
        if dialog.is_valid():
            dialog.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class AddUserRoom(APIView):
    # def get(self, request):
    #     users = User.objects.all()
    #     serializer = UserSerializer(users,many=True)
        
    #     return Response(serializer.data)
    
    def post(self,request):
        room = request.data.get('room')
        user = request.data.get('user')

        try:
            room = Room.objects.get(id=room)
            room.invited.add(user)
            room.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer