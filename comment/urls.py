from . import views
from django.urls import path

urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment'),

]
