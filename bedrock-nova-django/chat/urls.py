from django.urls import path
from .views import chat_with_nova

urlpatterns = [
    path("chat/", chat_with_nova),
]
