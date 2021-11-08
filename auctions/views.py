from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "items": Listing.objects.all()
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'base_price', 'image_url', 'category']

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['title'].widget.attrs['style'] = 'width:500px; height:35px;'
        self.fields['image_url'].widget.attrs['style'] = 'width:500px; height:35px;'
        self.fields['description'].widget.attrs['style'] = 'width:500px;'
        self.fields['category'].widget.attrs['style'] = 'width:200px;'


@login_required
def listing(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = ListingForm(request.POST)
        owner = User.objects.get(id=request.user.id)
        # Check if form data is valid (server-side)
        if form.is_valid():
            listing_item = form.save(commit=False)
            listing_item.owner = owner
            listing_item.save()
            return render(request, "auctions/details.html", {
                "item": listing_item
            })
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "auctions/create.html", {
                "form": ListingForm()
            })
    return render(request, "auctions/create.html", {
        "form": ListingForm()
    })


def item(request, item_id, message=None):
    item_details = Listing.objects.get(id=item_id)
    bids = item_details.bid.all()
    highest_bid = bids.last()
    if not highest_bid:
        user = User.objects.get(id=request.user.id)
        highest_bid = Bid(listing_id=item_details, user_id=user, price=item_details.base_price)
    comments = item_details.item_comment.all()
    return render(request, "auctions/details.html", {
        "item": item_details,
        "bids": bids,
        "comments": comments,
        "highest_bid": highest_bid,
        "message": message
    })


@login_required
def bid(request):
    if request.method == "POST":
        curr_price = request.POST['curr_price']
        price = request.POST['price']
        thing_id = request.POST['listing']
        if price > curr_price:
            auction = Listing.objects.get(id=thing_id)
            user = User.objects.get(id=request.user.id)
            curr_bid = Bid(listing_id=auction, user_id=user, price=price)
            curr_bid.save()
            return item(request, thing_id)
        else:
            # return HttpResponse("Your bid should be greater than the current highest bid")
            messages.error(request, "Your bid should be greater than the current highest bid")
            return item(request, thing_id, message="Your bid should be greater than the current highest bid!!!")


@login_required
def comment(request):
    if request.method == "POST":
        item_id = request.POST['listing_id']
        thing = Listing.objects.get(id=item_id)
        user = User.objects.get(id=request.user.id)
        com = request.POST['comment']
        comm = Comment(listing_id=thing, user_id=user, comment=com)
        comm.save()
        return item(request, item_id)


@login_required
def watchlist(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        item_id = request.POST['listing']
        thing = Listing.objects.get(id=item_id)
        thing.watchlist.add(user)
        return item(request, item_id)
