from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from users.views import Login, Logout
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="API APP Doc",
      default_version='v0.1',
      description="Proyecto de uso DRF",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="vergara_bruno@outlook.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('admin/', admin.site.urls),
    path('usuario/', include('users.api.urls')),
    path('producto/', include('products.api.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
