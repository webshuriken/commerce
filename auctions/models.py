from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField()
    description = models.CharField()
    value = models.DecimalField()
    image = models.URLField()
    user = models.ForeignKey()
    category = models.ForeignKey()

    # custom string representation
    def __str__(self):
        return f"ID: {self.id}: {self.title}\nDescription: {self.description}\nValue: {self.value}\nCreated by: {self.user}\n"