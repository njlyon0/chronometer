# Import needed libraries
from django.db import DatabaseError, connection
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

# Import classes defined in this repo
from .services import project_totals


# Add page with a table of total hours per project
def totals(request: HttpRequest) -> HttpResponse:
    return render(request, "tracker/totals.html", {"projects": project_totals()})


# Add health page
def health(request: HttpRequest) -> JsonResponse:
    try:
        connection.ensure_connection()
    except DatabaseError:
        return JsonResponse({"status": "error", "db": "unreachable"}, status=503)
    return JsonResponse({"status": "ok"})
