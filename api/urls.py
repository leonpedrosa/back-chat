from rest_framework import routers
from unicodedata import name
from api.views import *

router = routers.DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'user', UserWithStatusViewSet, basename='user')
router.register(r'messages', MessageViewSet, basename='message')
urlpatterns = router.urls