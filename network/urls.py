
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit/<int:postid>", views.edit_post, name="edit_post"),
    path("profile/<str:profile_name>", views.profile_page, name="profile_page"),
    path("following", views.following, name="following"),
    path("like/<int:postid>", views.like_post, name="like_post")
]
