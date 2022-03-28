from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Path for an entry_title (e.g. wiki/entry_title) that will execute views.entry, taking the entry_title as a parameter
    path("wiki/<str:entry_title>", views.entry, name="entry"),
    # Path for search
    path("search", views.search, name="search"),
    # Path for random_entry
    path("random", views.random_entry, name="random"),
    # Path for creating a new entry
    path("new_entry", views.new_entry, name="new_entry"),
    # Path for saving an entry
    path("save_entry", views.save_entry, name="save_entry")
]
