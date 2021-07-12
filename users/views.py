from os import stat
import re
from datetime import datetime
from users.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from users.api.serializers import UserTokenSerializer


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # llamamos al serializador 'AuthTokenSerializer' definido en ObteinAuthToken
        login_serializer = self.serializer_class(data=request.data, context={'request': request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'mensaje': 'Inicio de sesion exitoso'
                    }, status=status.HTTP_201_CREATED)
                else:
                    all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({
                            'token': token.key,
                            'user': user_serializer.data,
                            'mensaje': 'Inicio de sesion exitoso'
                        }, status=status.HTTP_201_CREATED)
                    """
                    si ya se ha iniciado sesion le bloqueo continuar
                    token.delete()
                    return Response({"mensaje": "Ya se ha iniciado sesion"}, 
                                    status=status,status.HTTP_409_CONFLICT)
                    """
            else:
                return Response({'message': 'Usuario no permitido'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Usuario o contraseña incorrecta'},
                            status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def get(self, request, *args, **kwagrs):
        try:
            token = request.GET.get('token')
            token =  Token.objects.filter(key=token).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                session_message = "Sesiones de usuario eliminadas"
                token_message = "Token eliminado"
                return Response({"token_messge": token_message, "session_message": session_message},
                                status=status.HTTP_200_OK)
            return Response({"error": "No se ha encontrado un usuario con estas credenciales"},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "No se ha encontrado el token en la peticion"},
                            status=status.HTTP_409_CONFLICT)
