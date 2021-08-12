from . import views
from django.urls import path

urlpatterns = [
    path('answer', views.answer, name='answer')
]