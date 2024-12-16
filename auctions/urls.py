from django.urls import path

from . import views


app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:category_id>", views.index, name="index_with_category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_listing", views.add_listing, name="add_listing"),
    # the path is only to be used to update the watchlist listing
    path("watchlist/<int:listing_id>", views.watch_listing, name="watchlist_listing"),
    # path only to be used to cloes a listing
    path("close_listing", views.close_listing, name="close_listing"),
]
