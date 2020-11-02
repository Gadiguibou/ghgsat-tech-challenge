from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator


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
