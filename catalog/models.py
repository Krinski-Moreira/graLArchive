from django.db import models

# Create your models here.

from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

class Lens(models.Model):
    Name = models.CharField(
        max_length = 30,
        unique = True,
        help_text = "Gravitational lens of a quasar"
    )

    RA_mean = models.DecimalField(
        max_digits = 11,
        decimal_places = 8
    )

    DEC_mean = models.DecimalField(
        max_digits = 10,
        decimal_places = 8
    )

    Author = models.CharField(
        max_length = 20,
        help_text = "Year and author of published paper"
    )

    BibCode = models.CharField(
        max_length = 20,
        help_text = "Year and author of published paper"
    )

    class Boolean_class(models.TextChoices):
        TRUE = "TRUE"
        FALSE = "FALSE"

    GraL = models.CharField(
        max_length=5,
        choices=Boolean_class
    )

    Max_separation = models.FloatField()

    def __str__(self):
        """String for representing the Model object."""
        return self.Name

    def get_absolute_url(self):
        """Returns the url to access a particular lens."""
        return reverse('lens-name', args=[str(self.Name)])


class LensComponent(models.Model):
    Name = models.ForeignKey(Lens, on_delete=models.CASCADE)

    Component = models.CharField(
        max_length = 5
    )

    RA_best = models.DecimalField(
        max_digits = 11,
        decimal_places = 8
    )

    DEC_best = models.DecimalField(
        max_digits = 10,
        decimal_places = 8
    )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.Name} {self.Component}'
