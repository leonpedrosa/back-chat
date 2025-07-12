#api/jwt_auth.py
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
import jwt


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser
        from django.conf import settings
        from django.contrib.auth import get_user_model
        from jwt import decode as jwt_decode
        from rest_framework_simplejwt.tokens import UntypedToken
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

        try:
            # Extrair token da query string (ex: ?token=abc123)
            token = scope.get('query_string')

            if token is None:
                scope["user"] = AnonymousUser()
                return await super().__call__(scope, receive, send)

            # Valida a assinatura e o tempo de expiração do token
            UntypedToken(token)

            # Decodifica o payload para extrair o user_id
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_data.get("user_id")

            # Busca o usuário correspondente
            user = await get_user(user_id)
            scope["user"] = user
        except (InvalidToken, TokenError, jwt.DecodeError, jwt.ExpiredSignatureError):
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)


# Helper async para buscar o usuário
from asgiref.sync import sync_to_async

@sync_to_async
def get_user(user_id):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import AnonymousUser
    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()