from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


#
class Person(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


#
class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name

# 
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

    def clean(self) -> None:
        if self.week_of and self.week_of.weekday() != 0:
            raise ValidationError({"week_of": "week_of must be a Monday."})

    def __str__(self) -> str:
        return f"{self.person} / {self.project} / {self.week_of}: {self.hours}h"
