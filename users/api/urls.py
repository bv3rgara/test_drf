from django.urls import path
from users.api.views import UserAPIView, user_list_view, user_detail_view

urlpatterns = [
    path('usuariox/', UserAPIView.as_view(), name='list_usuario_class'),
    path('usuario/', user_list_view, name='list_usuario'),
    path('usuario/<int:pk>/', user_detail_view, name='detail_usuario'),
]
