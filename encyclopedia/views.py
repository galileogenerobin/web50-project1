from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Render an entry page
def entry(request, entry_title):
    # Check if a valid entry exists for the given entry_title
    entry_content = util.get_entry(entry_title)

    # If there is a valid entry
    if entry_content is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry_title,
            "entry_content": entry_content
        })
    else:
        # Render the apology page
        return render(request, "encyclopedia/error.html")


# Handle search results
def search(request):
    # Get the search query
    search_query = request.GET['q']

    # Check for entries that have the search query as a substring (or could be the exact match)
    # We need to convert the serach query and the entry to lower case so that our search is not case sensitive
    search_results = [entry for entry in util.list_entries() if search_query.lower() in entry.lower()]

    # Check if there is an exact match, not case sensitive
    for entry in search_results:
        if search_query.lower() == entry.lower():
            # Redirect to the results page for that entry
            return HttpResponseRedirect("wiki/{}".format(entry))
    
    # Otherwise, we render the search results in the index page
    return render(request, "encyclopedia/search.html", {
        "search_query": search_query,
        "search_results": search_results
    })