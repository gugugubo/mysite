from . import views
from django.urls import path

urlpatterns = [
    path('like', views.likes, name='likes'),

]
