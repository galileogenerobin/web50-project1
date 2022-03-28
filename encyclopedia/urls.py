from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Creating a path for an entry_title (e.g. wiki/entry_title) that will execute views.entry, taking the entry_title as a parameter
    path("wiki/<str:entry_title>", views.entry, name="entry"),
    # Creating a path for search
    path("search", views.search, name="search"),
    # Creating a path for random_entry
    path("random", views.random_entry, name="random")
]
