# Import needed libraries
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


# Table for a person who logs hours (one row per uniquely-named person)
class Person(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


# Table for a uniquely-named project against which hours are logged
class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


# Table for hours that one person spent on one project in one week
class WeeklyHours(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="weekly_hours"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="weekly_hours"
    )
    week_of = models.DateField()
    hours = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name_plural = "weekly hours"
        ordering = ["-week_of"]
        # Add a constraint that each combination of person/project/week must be unique
        constraints = [
            models.UniqueConstraint(
                fields=["person", "project", "week_of"],
                name="unique_person_project_week",
            )
        ]

    def clean(self) -> None:
        if self.week_of and self.week_of.weekday() != 0:
            raise ValidationError({"week_of": "week_of must be a Monday."})

    def __str__(self) -> str:
        return f"{self.person} / {self.project} / {self.week_of}: {self.hours}h"
