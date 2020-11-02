# General Imports
from django.db import models
from django.utils import timezone
import os

# Imports for Target class
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
import requests

# Imports for Observation class
from django.db.models.deletion import CASCADE


def upload_to(_instance, filename):
    """
    Helper function to define the upload location of media files.
    """
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    return f"{now:%Y%m%d%H%M%S}{extension}"


class Target(models.Model):
    """
    Defines a basic format for interacting with a point in geographic coordinates. 
    """

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

    def get_image(self) -> Image:
        """
        Queries the mapquest API for a static map of approximately 10 x 5 km centered on the target's coordinates.

        Returns 
        -------
        Image
            A PIL Image object containing the satellite image of the target.
        """
        # This would normally be stored elsewhere (e.g. as an environment
        # variable) but for the sake of making this demonstration run smoothly,
        # I'll be leaving it here for now.
        api_key = "JKaBPEPARkPpJLsxoP9t03GtCLJUnQ6b"

        api_base_url = "http://www.mapquestapi.com/staticmap/v4/getmap"

        api_url = "{0}?key={1}&size=514,257&zoom=13&type=sat&center={2},{3}".format(
            api_base_url, api_key, self.latitude, self.longitude
        )

        response = requests.get(api_url)

        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            raise Exception("Request to mapquest API was unsuccessful")

    def overlay(self, img: Image, overlay: Image) -> Image:
        """
        Overlays a given Image object with transparency over another.

        Returns
        -------
        Image
            A Image object with the two input pictures overlaid.
        """
        img.paste(overlay, (0, 0), overlay)
        return img

    def save_image(self, path):
        """
        Save an image of the target to a given local path.
        """
        self.get_image().save(path)

    def save_overlaid(self, overlay, path):
        """
        Save the resulting image of a target overlaid with the given plume image.
        """
        self.overlay(self.get_image(), overlay).save(path)


class Observation(models.Model):
    """
    The Observation class links the image of a given observation of a plume with the
    associated Target object over which it was recorded.
    """

    target = models.ForeignKey(Target, on_delete=CASCADE)
    image = models.ImageField(upload_to=upload_to)

    def __str__(self) -> str:
        return self.target.name
