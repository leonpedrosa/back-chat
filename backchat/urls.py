from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Chat Web Socket",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="leondeoliveirapedrosa@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
    url=settings.URL_API,
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
