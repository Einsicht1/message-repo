from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from message.views import MessageAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Title",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("api/v1/messages/", MessageAPIView.as_view(), name="messages"),
    path("api/v1/messages/<int:pk>/", MessageAPIView.as_view(), name="message"),
]
