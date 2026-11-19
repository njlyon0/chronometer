# Import needed libraries
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Import classes defined in this repo
from .services import project_totals


# Add page with a table of total hours per project
def totals(request: HttpRequest) -> HttpResponse:
    return render(request, "tracker/totals.html", {"projects": project_totals()})
