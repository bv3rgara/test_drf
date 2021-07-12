from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
# from rest_framework.authtoken.models import Token


class ExpiringTokenAuthentication(TokenAuthentication):
    expired = False
    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        # cualquier de las 2 formas
        #left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS - time_elapsed.total_seconds())
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            expired = True
            user = token.user
            token.delete()
            # se pueden borrar las sesiones
            token = self.get_model().objects.create(user=user)
        return is_expire, token

    def authenticate_credentials(self, key):
        mesaage, token, user = None, None, None
        try:
            #token = Token.objects.get(key=key) esta clase tiene implentado 
            # una func que devueleve el modelo sino esta definido devuelve el model Token
            token = self.get_model().objects.select_related('user').get(key=key)
            user = token.user
        except self.get_model().DoesNotExist:
            #raise AuthenticationFailed('Token invalido')
            mesaage = "Token invalido"
        if token is not None:
            if not token.user.is_active:
                #raise AuthenticationFailed('Usuario invalido o eliminado')
                mesaage = 'Usuario invalido o eliminado'
            is_expired = self.token_expire_handler(token)
            if is_expired:
                #raise AuthenticationFailed('Su token ha expirado')
                mesaage = "Su token ha expirado"
        return (user, token, mesaage, self.expired)