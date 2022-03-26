from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Creating a path for an entry_title (e.g. wiki/entry_title) that will execute views.entry, taking the entry_title as a parameter
    path("wiki/<str:entry_title>", views.entry, name="entry")
]
