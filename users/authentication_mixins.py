from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from users.authentication import ExpiringTokenAuthentication
from rest_framework.authentication import get_authorization_header


class Authentication(object):
    """
    def dispatch(self, request, *args, **kwargs):
    if request.method == 'GET':
        return self.get(*args, **kwargs)
    elif request.method == 'POST':
        return self.post(*args, **kwargs)
    elif ... 
    Cuando una URL de solicitud coincide con una URL en su archivo urls.py,
    django pasa esa solicitud a la vista que especificó. La solicitud solo
    se puede pasar a funciones invocables. Es por eso que cuando usa vistas
    basadas en clases, usa el as_view()método. El as_view()método devuelve
    una función que se puede llamar. Esta función luego crea una instancia
    de la clase de vista y llama a su dispatch()método. El método de envío
    luego mira la solicitud y decide si el método GET o POST de la clase de
    vista debe manejar la solicitud.
    """
    user = None
    user_token_expired = False
    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                return None
            token_expired = ExpiringTokenAuthentication()
            user, token, message, self.user_token_expired = token_expired.authenticate_credentials(token)
            if user != None and token != None:
                self.user = user
                return user
            return message
        return None

    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(request)
        if user is not None:
            if type(user) == str:
                response = Response({"Error": user, 'expired': self.user_token_expired},
                                    status=status.HTTP_401_UNAUTHORIZED)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'aplication/json'
                response.renderer_context = {}
                return response
            if not self.user_token_expired:
                return super().dispatch(request, *args, **kwargs)
        response =  Response({"Error": "No se han enviado las credenciales",
                            "expired": self.user_token_expired},
                             status=status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'aplication/json'
        response.renderer_context = {}
        return response
