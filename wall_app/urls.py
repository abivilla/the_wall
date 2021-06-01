from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.success),
    path('logout', views.logout),
    path('create_post', views.create_post),
    path('create_comment/<int:id>', views.create_comment)
]
