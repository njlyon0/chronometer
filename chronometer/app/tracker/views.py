# Import needed libraries
from django.db.models import DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Import classes defined in this repo
from .models import Project


# Add page with a table of total hours per project
def totals(request:HttpRequest) -> HttpResponse:
    projects = Project.objects.annotate(
        total_hours=Coalesce(
            Sum("weekly_hours__hours"), Value(0), output_field=DecimalField()
        )
    ).order_by("name")
    return render(request, "tracker/totals.html", {"projects": projects})
