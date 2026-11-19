# Import needed libraries
from django.db.models import DecimalField, QuerySet, Sum, Value
from django.db.models.functions import Coalesce

# Import classes defined in this repo
from .models import Project


# Get every project with its total hours (0 if it has none), sorted by name
def project_totals() -> QuerySet[Project]:
    return Project.objects.annotate(
        total_hours=Coalesce(
            Sum("weekly_hours__hours"), Value(0), output_field=DecimalField()
        )
    ).order_by("name")
