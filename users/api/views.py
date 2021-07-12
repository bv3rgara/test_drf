from decimal import Context
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from users.models import User
from users.api.serializers import UserListSerializer, TestUserSerializer, UsersSerializer

class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all().values('id', 'username', 'name', 'password')
        users_serializers = UserListSerializer(users, many=True)
        return Response(users_serializers.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def user_list_view(request):
    if request.method == 'GET':
        users = User.objects.all().values('id', 'username', 'name', 'password')
        users_serializers = UserListSerializer(users, many=True)
        #test_data = {
        #    "name": "pochitox",
        #    "email": "xxxxxxc@gmail.com"
        #}
        #test_user = TestUserSerializer(data=test_data, context=test_data)
        #if test_user.is_valid():
        #    test_user.save()
        #    print("validado000000000000000000000000000000000000000000")
        #else:
        #    print("NOOOOOOOOOOOOOOOOOOOOOOO-----------------------", test_user.errors)
        return Response(users_serializers.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        users_serializers = UsersSerializer(data=request.data)
        print("NOOOOOOOOOOOOOOOOOOOOOOO-----------------------")
        if users_serializers.is_valid():
            print("SIIIIIIIIIIIIIIIIIII-----------------------")
            users_serializers.save()
            return Response(users_serializers.data, status=status.HTTP_201_CREATED)
        return Response(users_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_view(request, pk):
    try:
        user = User.objects.get(id=pk)
    except Exception as e:
        dic = {'mensaje': 'Usuario no encontrado!'}
        return Response(dic, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        user_serializers = UsersSerializer(user)
        return Response(user_serializers.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        user_serializers = UsersSerializer(user, data=request.data)
        if user_serializers.is_valid():
            user_serializers.save()
            return Response(user_serializers.data, status=status.HTTP_200_OK)
        return Response(user_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        dic = {'mensaje': 'Usuario eliminado!'}
        return Response(dic, status=status.HTTP_200_OK)
