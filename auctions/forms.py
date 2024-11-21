from django import forms
from .models import Category

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter listing title'}))
    description = forms.CharField(label="Description", max_length=1000, widget=forms.Textarea(attrs={'placeholder': 'Describe your listing'}))
    starting_bid = forms.DecimalField(label="Starting Bid", max_digits=8, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': 'Enter starting bid'}))
    image_url = forms.URLField(label="Image URL", max_length=512, required=False, widget=forms.URLInput(attrs={'placeholder': 'Enter image URL'}))
    # DB query to get all categories
    category = forms.ModelChoiceField(queryset=Category.objects.all())
