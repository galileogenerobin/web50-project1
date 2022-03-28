import random
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import markdown2

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
        # Convert to HTML using markdown2
        entry_content = markdown2.markdown(entry_content)
        
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
            return redirect('wiki/{}'.format(entry))
    
    # Otherwise, we render the search results in the index page
    return render(request, "encyclopedia/search.html", {
        "search_query": search_query,
        "search_results": search_results
    })


# Create a new entry page
def new_entry(request):
    return render(request, "encyclopedia/new_page.html", {
        "entry_title": '',
        "entry_content": '',
        "page_exists": False
    })


# Save an entry given an entry title and entry content; we will use this both for Create New Entry and Edit Entry
def save_entry(request):
    # We will only process POST requests
    if request.method == 'POST':
        entry_title = request.POST['title']
        entry_content = request.POST['content']

        # Check all existing entries
        for entry in util.list_entries():
            # Check if an existing entry already exists with the same title. If so, present an error message but retain the user's input
            if entry.lower() == entry_title.lower():
                return render(request, "encyclopedia/new_page.html", {
                    "entry_title": entry_title,
                    "entry_content": entry_content,
                    "page_exists": True
                })

        # Otherwise, save the entry and redirect to the home page (using the Post-Redirect-Get Pattern to avoid repeating the request via F5 / Refresh)
        util.save_entry(entry_title, entry_content)
        # Redirect to the home page
        return redirect('index')


# Redirect to a random wiki entry
def random_entry(request):
    # Select a random entry from our list of entries, and redirect to that page
    return redirect('wiki/{}'.format(random.choice(util.list_entries())))