from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import *
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.serializers import *
from api.models import *

class AuthViewSet(ViewSet):

    @swagger_auto_schema(
        tags=['auth'],
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    @action(methods=['POST'], detail=False, url_path='login', permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': username,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            )
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class UserWithStatusViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserWithStatusSerializer



class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        contact_id = self.request.query_params.get('contact')
        if contact_id:
            return Message.objects.filter(
                sender_id__in=[user.id, contact_id],
                recipient_id__in=[user.id, contact_id]
            )
        return Message.objects.none()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

