from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


# custom validator used by Listing model
def validate_price(value):
    if value < 0 or value == 0:
        raise ValidationError(f"{value} is not a valid price")

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    value = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_price])
    image = models.URLField(blank=True, null=True)
    user = models.ForeignKey(default=None, on_delete=models.CASCADE, related_name="creator")
    category = models.ForeignKey(default=None, on_delete=models.CASCADE, related_name="category")

    # custom string representation
    def __str__(self):
        return f"ID: {self.id}: {self.title}\nDescription: {self.description}\nValue: {self.value}\nCreated by: {self.user}\n"