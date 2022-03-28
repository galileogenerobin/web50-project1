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


# Save an entry given an entry title and entry content; we will use this both for Create New Entry and Edit Entry
def update_entry(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new_page.html", {
        "entry_title": '',
        "entry_content": '',
        "page_exists": False
        })
    # We will only process POST requests
    elif request.method == 'POST':
        entry_title = request.POST['title']
        entry_content = request.POST['content']
        is_new_entry = True if request.POST['new-or-edit'] == 'New' else False

        # Check flag if new entry or editing existing entry
        if is_new_entry:
            # Check all existing entries
            for entry in util.list_entries():
                # Check if an existing entry already exists with the same title. If so, present an error message but retain the user's input
                if entry.lower() == entry_title.lower():
                    return render(request, "encyclopedia/new_page.html", {
                        "entry_title": entry_title,
                        "entry_content": entry_content,
                        "page_exists": True
                    })
                    # We stop here and don't save any changes

        # Otherwise, save the entry (i.e. editing existing entry, or creating new entry without a duplicate)
        util.save_entry(entry_title, entry_content)
        
        # We use the Post-Redirect-Get Pattern to avoid repeating the request via F5 / Refresh
        # If new entry, redirect to the home page
        if is_new_entry: return redirect('index')
        # Otherwise, if editing existing entry, redirect to the entry page
        return redirect('wiki/{}'.format(entry_title))


# Edit and existing entry
def edit_entry(request):
    # We will only process POST requests (to avoid handling manual URL get requests)
    if request.method == 'POST':
        entry_title = request.POST['title']
        # Check if there is an existing entry
        entry_content = util.get_entry(entry_title)
        if entry_content is not None:
            return render(request, 'encyclopedia/edit_page.html', {
                'entry_title': entry_title,
                'entry_content': entry_content
            })
  
    # Otherwise (i.e. GET method, or invalid entry title), render the error page
    return render(request, 'encyclopedia/error.html')


# Redirect to a random wiki entry
def random_entry(request):
    # Select a random entry from our list of entries, and redirect to that page
    return redirect('wiki/{}'.format(random.choice(util.list_entries())))