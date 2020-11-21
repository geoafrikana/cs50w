from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.article, name ="article"),
    path('searcher', views.searcher, name='searcher'),
    path('newpage', views.newpage, name='newpage'),
    path('editcontent', views.editcontent, name='editcontent'),
    path('save_edit', views.save_edit, name='save_edit'),
    path('random_post', views.random_post, name='random_post')
]
