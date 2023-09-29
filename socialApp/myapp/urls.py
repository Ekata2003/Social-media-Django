"""socialApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.db import models
from .import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name="index"),
    path('createPost', views.createPost, name="createPost"),
    path('addComment/<int:post_id>', views.addComment, name="addComment"),
    path('like/<int:post_id>', views.like, name="like"),
    path('signup', views.handleSignup, name="handleSignup"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path("<str:username>", views.profile, name='profile'),
    path("<str:username>/follow", views.follow, name='follow'),
    path("<str:username>/unfollow", views.unfollow, name='unfollow')
]
