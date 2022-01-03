from datetime import date, datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from auctions.forms import ProductsForm
from time import gmtime, strftime
from django.utils import timezone

from decimal import *
from .models import *
from .forms import *


def index(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, "auctions/index.html", {
            "all_products": Products.objects.filter(status=True),
            "saveds": user.watchlist.all().count()
        })
    else:
        return render(request, "auctions/index.html", {
            "all_products": Products.objects.filter(status=True)
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
    return HttpResponseRedirect(reverse("login"))


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


@login_required(login_url='login')
def products_all(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, "auctions/products_all.html", {
            "all_products": Products.objects.filter(status=True),
            "closed_products": Products.objects.filter(status=False),
            "saveds": user.watchlist.all().count()
        })


@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        product = ProductsForm(request.POST, request.FILES)
        if product.is_valid():
            new_product = product.save(commit=False)
            new_product.user_seller = request.user

            if new_product.pictureURL is None or new_product.pictureUpload is True:
                new_product.pictureURL = "https://media.istockphoto.com/vectors/no-image-available-sign-vector-id922962354?k=6&m=922962354&s=612x612&w=0&h=_KKNzEwxMkutv-DtQ4f54yA5nc39Ojb_KPvoV__aHyU="

            elif new_product.description is None:
                new_product.description = "No description."

            else:
                new_product.pictureUpload
            new_product.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        user = request.user
        return render(request, "auctions/create.html", {
            "product_form": ProductsForm(),
            "saveds": user.watchlist.all().count()
        })


@login_required(login_url='login')
def product_page(request, product_pk):
    user = request.user
    itemObject = Products.objects.get(id=product_pk)
    commentsObject = Comments.objects.filter(
        products=product_pk).order_by('-time').all()
    showtime = timezone.now()
    print(timezone.now())
    if itemObject.bid_timer is not None and itemObject.bid_timer <= showtime:
        itemObject.status = False
        itemObject.save()
    if itemObject.status == False:
        user.watchlist.remove(itemObject)
        user.save()
    if request.user.is_authenticated:
        watchlistcheck = request.user.watchlist.filter(pk=product_pk).exists()
        if request.method == "POST" and request.user.is_authenticated:
            form = BidsForm(request.POST)
            price = Decimal(request.POST.get('price'))
            higherBid = itemObject.higherBid
            if higherBid is not None and higherBid.price.compare(price) == -1:
                if form.is_valid:
                    bidder = form.save(commit=False)
                    bidder.user = request.user
                    bidder.products = itemObject
                    itemObject.higherBid = bidder
                    bidder.save()
                    itemObject.save()
                    messages.success(request, 'Bid submitted successfully.')
                return HttpResponseRedirect(reverse("product", kwargs={'product_pk': product_pk}))
            elif higherBid is not None and higherBid.price.compare(price) != -1:
                messages.error(request, 'The bid must be greater than the currently bid.')
                return HttpResponseRedirect(reverse("product", kwargs={'product_pk': product_pk}))
            elif higherBid is None and price.compare(itemObject.price) == 1:
                if form.is_valid:
                    bidder = form.save(commit=False)
                    bidder.user = request.user
                    bidder.products = itemObject
                    itemObject.higherBid = bidder
                    bidder.save()
                    itemObject.save()
                return HttpResponseRedirect(reverse("product", kwargs={'product_pk': product_pk}))
            else:
                return HttpResponseRedirect(reverse("product", kwargs={'product_pk': product_pk}))
        else:

            userListBid = Bid.objects.filter(products=product_pk)
            countingBids = Bid.objects.filter(products=product_pk).count()
            higherBid = Bid.objects.filter(
                products=product_pk).order_by('price')
            return render(request, "auctions/product_page.html", {
                "product": itemObject,
                "status": itemObject.status,
                "comments": commentsObject,
                "comments_form": CommentsForm(),
                "bid_form": BidsForm(),
                "higherBid": higherBid,
                "watchlistcheck": watchlistcheck,
                "countingBids": countingBids,
                "userListBid": userListBid,
                "saveds": user.watchlist.all().count()
            })


def edit_listing(request, product_pk):
    user = request.user
    itemObj = Products.objects.get(id=product_pk)
    form = ProductsForm(instance=itemObj)
    if request.method == "POST":
        form = ProductsForm(request.POST, instance=itemObj)
        if form.is_valid():            
            form.save()
            return HttpResponseRedirect(reverse("product", kwargs={'product_pk': product_pk}))
    return render(request, "auctions/update.html", {
        "form": form,
        "saveds": user.watchlist.all().count()
    })


def close_bid(request, product_pk):
    if request.method == "POST":
        itemObj = Products.objects.get(id=product_pk)
        itemObj.status = False
        itemObj.save()
    return HttpResponseRedirect(reverse("product", kwargs={'product_pk': product_pk}))


def watchlist_add(request, product_pk):
    if request.method == "POST":
        assert request.user.is_authenticated
        user = request.user
        itemObj = Products.objects.get(pk=product_pk)
        if user.watchlist.filter(pk=product_pk).exists():
            user.watchlist.remove(itemObj)
        else:
            user.watchlist.add(itemObj)
    return HttpResponseRedirect(reverse("product", kwargs={'product_pk': product_pk}))


@login_required(login_url='login')
def watchlist_page(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, "auctions/watchlist_page.html", {
            "watchlist": request.user.watchlist.all(),
            "saveds": user.watchlist.all().count()
        })


def comments_action(request, product_pk):
    itemObject = Products.objects.get(id=product_pk)
    comment_form = CommentsForm(request.POST)
    if request.method == "POST":
        comments = comment_form.save(commit=False)
        comments.user = request.user
        comments.products = itemObject
        comments.save()
        return HttpResponseRedirect(reverse("product", kwargs={'product_pk': product_pk}))


@login_required(login_url='login')
def categories(request):
    user = request.user
    categories = list(set(
        [Products.category for Products in Products.objects.all() if Products.category]))
    return render(request, "auctions/categories.html", {
        'categories': categories,
        "saveds": user.watchlist.all().count()
    })


@login_required(login_url='login')
def categories_list(request, category):
    user = request.user
    return render(request, "auctions/index.html", {
        'all_products': Products.objects.filter(status=True, category=category),
        "saveds": user.watchlist.all().count()
    })
