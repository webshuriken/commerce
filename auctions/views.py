from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import NewListingForm
from .models import User, Listing, Category


def index(request, category_id=None):
    if category_id:
        # load listings by category
        listings = Listing.objects.filter(category_id=category_id, active=True)
        category = Category.objects.get(id=category_id).name
        return render(request, "auctions/index.html", {
            "category": category,
            "listings": listings
        })
    else:
        # load all active listings (default view)
        listings = Listing.objects.filter(active=True)
        category = 'All'
        return render(request, "auctions/index.html", {
            "category": category,
            "listings": listings
        })


def categories(request):
    # load all categories
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def listing(request, listing_id):
    # load listing by id and all comments
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.listing_comments.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })


@login_required(login_url='/login')
def watchlist(request):
    # load watchlist items by user id
    user = User.objects.get(pk=request.user.id)
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


@login_required(login_url='/login')
def add_listing(request):
    # POST request
    if request.method == "POST":
        # bound form with posted form data
        form = NewListingForm(request.POST)
        if form.is_valid():
            # get form data
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]

            # create new listing
            listing = Listing(title=title, description=description, value=starting_bid, image=image_url, category=category, user=request.user)
            listing.save()

            return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
        else:
            # return form to user with errors
            return render(request, "auctions/add_listing.html", {
                "form": form
            })

    # GET request
    form = NewListingForm()
    return render(request, "auctions/add_listing.html", {
        "form": form
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
