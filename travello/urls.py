from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("apartments", views.apartments, name="apartments"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("addToWishlist", views.addToWishlist, name="addToWishlist"),
    path("chatbot", views.chatbot, name="chatbot")
    ]
