# General Imports
from django.db import models
from django.utils import timezone
import os


# Imports for Target class
from django.core.validators import MaxValueValidator, MinValueValidator

# Imports for Observation class
from django.db.models.deletion import CASCADE


def upload_to(_instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    return f"{now:%Y%m%d%H%M%S}{extension}"


class Target(models.Model):
    name = models.CharField(max_length=60, unique=True)
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        validators=[MaxValueValidator(90), MinValueValidator(-90)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MaxValueValidator(180), MinValueValidator(-180)],
    )

    def __str__(self) -> str:
        return self.name


class Observation(models.Model):
    target = models.ForeignKey(Target, on_delete=CASCADE)
    image = models.ImageField(upload_to=upload_to)

    def __str__(self) -> str:
        return self.target.name
