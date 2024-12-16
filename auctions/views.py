from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ValidationError
from .forms import NewListingForm, NewCommentForm, NewBidForm
from .models import User, Listing, Category, Watchlist, Comment, Bid


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
    # check if user is watching the listing
    watching = Watchlist.objects.filter(user=request.user.id, listing=listing_id)

    # POST request
    if request.method == "POST":
        # check if comment form was submitted
        if 'submit_comment' in request.POST:
            # populate comment form with posted data and create fresh bid form
            commentForm = NewCommentForm(request.POST)
            bidForm = NewBidForm()
            if commentForm.is_valid():
                comment = commentForm.cleaned_data["comment"]
                # create new comment
                new_comment = Comment(comment=comment, user=request.user, listing=listing)

                try:
                    # apply model validation
                    new_comment.full_clean()
                    new_comment.save()
                    return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
                except ValidationError as e:
                    # return commentForm to user with errors
                    commentForm.add_error("comment", e.message_dict["comment"])

        elif 'submit_bid' in request.POST:
            # populate bid form with posted data and create fresh comment form
            bidForm = NewBidForm(request.POST)
            commentForm = NewCommentForm()
            if bidForm.is_valid():
                # get all bids for this listing
                bids = listing.listing_bids.all()
                # get bid value from form
                bid = bidForm.cleaned_data["bid"]
                # create new bid
                newBid = Bid(value=bid, user=request.user, listing=listing)

                try:
                    # apply model validation
                    newBid.full_clean()

                    ## BID REQUIREMENTS:

                    # 1. bid must be the same or higher than listing value
                    if bid < listing.value:
                        raise Exception("Bid can not be lower than item value")
                    
                    # 2. bid must be higher than current highest bid
                    if bids.exists():
                        # uses a generator expression to get the highest bid value
                        highest_bid = max(b.value for b in bids)
                        if bid <= highest_bid:
                            raise Exception("Bid must be higher than current highest bid")
                
                except ValidationError as e:
                    # return bidForm to user with error
                    bidForm.add_error("bid", "Bid must be the same or higher than current value")
                except Exception as e:
                    # return bidForm to user with error
                    bidForm.add_error("bid", e)
                else:
                    # all in order so lets save the bid
                    newBid.save()
                    return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
    else:
        # create new comment and bid form
        commentForm = NewCommentForm()
        bidForm = NewBidForm()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "watching": True if watching.exists() else False,
        "commentForm": commentForm,
        "bidForm": bidForm
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
            
            try:
                # apply model validation
                listing.full_clean()
                listing.save()
                return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
            except ValidationError as e:
                # return form to user with errors
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
                return render(request, "auctions/add_listing.html", {
                    "form": form
                })
    else:
        # GET request
        form = NewListingForm()
        return render(request, "auctions/add_listing.html", {
            "form": form
        })


# post required to aceess this view
@require_POST
def watch_listing(request, listing_id):
    user_watching = Watchlist.objects.filter(user=request.user.id, listing=listing_id)
    response = { 'success': False, 'message': 'The Database could not be updated' }
    if user_watching:
        user_watching.delete()
        response['success'] = True
        response['type'] = 'REMOVE'
        response['message'] = 'Listing removed from watchlist'
    else:
        watching = Watchlist(user=User.objects.get(pk=request.user.id), listing=Listing.objects.get(pk=listing_id))
        watching.save()
        response['success'] = True
        response['type'] = 'ADD'
        response['message'] = 'Listing added to watchlist'

    return JsonResponse(response)

# post required to aceess this view
@require_POST
def close_listing(request):
    pass

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
