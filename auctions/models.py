from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from better_profanity import profanity
from decimal import Decimal


# custom validator used by Listing model
def validate_price(value):
    if value < 0 or value == 0:
        raise ValidationError(f"{value} is not a valid price")

# custom validator used by Listing model
def validate_profanity(text):
    if profanity.contains_profanity(text):
        raise ValidationError(f"Contains a bad word")

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100, validators=[validate_profanity])
    description = models.CharField(max_length=1000, validators=[validate_profanity])
    value = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_price])
    image = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="creator")
    # category = models.ForeignKey(default=None, on_delete=models.CASCADE, related_name="category")

    # custom string representation
    def __str__(self):
        return f"ID: {self.id}: {self.title}\nDescription: {self.description}\nValue: {self.value}\nCreated by: {self.user}\n"

class Comment(models.Model):
    comment = models.CharField(max_length=512, validators=[validate_profanity])
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE, related_name="listing_comments")

    def __str__(self):
        return f"ID: {self.id}: {self.comment} by user {self.user}\nFor listing: {self.listing}\n"

class Bid(models.Model):
    value = models.DecimalField()
    user = models.ForeignKey(User)
    listing = models.ForeignKey(Listing)

    def __str__(self):
        return f"ID:{self.id}: {self.value} bid by {self.user}\n"