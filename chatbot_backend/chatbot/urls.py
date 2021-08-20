from . import views
from django.urls import path

urlpatterns = [
    path('answer', views.answer, name='answer'),
    path('fashion/<user>', views.getFashionChatHistory, name='getFashionChatHistory'),
]
