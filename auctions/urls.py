from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("products", views.products_all, name="products_all"),
    path("create", views.create_listing, name="create"),
    path("product/<int:product_pk>", views.product_page, name="product"),
    path("comments/<int:product_pk>", views.comments_action, name="comments"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categories_list, name='categories_list'),
    path("watchlist/<int:product_pk>", views.watchlist_add, name="watchlist"),
    path("watchlist_add/<int:product_pk>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page"),
    path("close_bid/<int:product_pk>", views.close_bid, name="close_bid"),
    path("edit/<int:product_pk>", views.edit_listing, name="edit")
]
