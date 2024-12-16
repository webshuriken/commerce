from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from better_profanity import profanity


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

# It is not populated by the app user, but by the developer
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"ID: {self.id}: {self.name}\n"

class Listing(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, validators=[validate_profanity])
    description = models.CharField(max_length=1000, validators=[validate_profanity])
    value = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_price])
    image = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="creator")
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, related_name="category")
    winner = models.ForeignKey(User, default=None, on_delete=models.PROTECT, related_name="winner", blank=True, null=True)

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
    value = models.DecimalField(max_digits=7, decimal_places=2, validators=[validate_price])
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, default=None, on_delete=models.PROTECT, related_name="listing_bids")

    def __str__(self):
        return f"ID:{self.id}: {self.value} bid by {self.user}\n"

# Watchlist is a many-to-many relationship between User and Listing
class Watchlist(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE, related_name="watchlist_listings")

    def __inint__(self):
        return f"User: {self.user} is Watching : {self.listing}\n"
