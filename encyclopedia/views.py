from django.shortcuts import render

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
        return render(request, "encyclopedia/error.html", {"entry_title": entry_title})

