from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/emails/<int:email_id>/', consumers.EmailConsumer.as_asgi())
]