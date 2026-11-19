# Import needed libraries
from django.contrib import admin

# Import needed pieces of database
from .models import Person, Project, WeeklyHours


# Register person/project model
@admin.register(Person, Project)
class NamedAdmin(admin.ModelAdmin):
    search_fields = ["name"]


# Register weekly hours model
@admin.register(WeeklyHours)
class WeeklyHoursAdmin(admin.ModelAdmin):
    list_display = ["week_of", "person", "project", "hours"]
    list_filter = ["project", "person", "week_of"]
    autocomplete_fields = ["person", "project"]
    date_hierarchy = "week_of"
