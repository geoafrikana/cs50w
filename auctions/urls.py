from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create_listing" ),
    path("listing/<str:listing_id>/", views.view_listing, name="view_listing" ),
    path("<str:username>/watchlist/", views.watchlist, name="watchlist" ),
    path("<str:individual_cat>/", views.individual_cat, name="individual_cat" ),
    path("categories", views.categories, name="categories" ),
    
]
