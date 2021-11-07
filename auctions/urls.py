from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create listing", views.listing, name="listing"),
    path("item_details/<int:item_id>", views.item, name="item_details"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment")
]
