# Import needed libraries
from django.urls import path

# Import own code
from . import views

# Route the 'project totals' page
app_name = "tracker"
urlpatterns = [
    path("", views.totals, name="totals"),
]
