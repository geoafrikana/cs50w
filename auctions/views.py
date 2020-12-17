from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import methods
from .models import *


def index(request):
    products = Listing.objects.all()
    return render(request, "auctions/index.html", {"products":products})


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


def create_listing(request):

    if request.method == 'POST':
        listing_title = request.POST["listing_title"]
        bid_start = request.POST["bid_start"]
        image_url = request.POST["image_url"]
        listing_category = request.POST["listing_category"].lower()
        listing_description = request.POST["listing_description"]
        bidder = request.POST["user"]
        methods.save_listing(listing_title,bid_start,image_url,listing_category,listing_description,User.objects.filter(pk=bidder).first())
       
        bidder = User.objects.get(id=bidder)
        bidobj=Bid(listing=Listing.objects.get(title=listing_title), amount=bid_start, bidder=bidder)
        bidobj.save()
        
        return render(request, "auctions/create_listing.html", {"message" : 'saved successfully'})
        
    return render(request, "auctions/create_listing.html", {"message" : ''})

def view_listing(request, listing_id):
    product= Listing.objects.get(pk=listing_id)
    comments = Comment_on_listing.objects.filter(listing=product)
    list_creator= str(product.seller)
    bid = Bid.objects.get(listing=product)
    highest_bidder = bid.bidder
    print(highest_bidder)
    if request.method == "POST" and 'watch' in request.POST:
        product_id = request.POST["product"]
        user = request.POST["user"]
        watchaction = request.POST["watch"]
        product = Listing.objects.get(pk=product_id)
        user = User.objects.get(username=user)
        if watchaction == 'Watch':
            user.watchlist.add(product)
            exists=True
        else:
            user.watchlist.remove(product)
            exists=False
        if product:
            return render(request, 'auctions/view_listing.html', {'product': product, 'comments':comments, 'exists':exists, 'list_creator':list_creator})
   
    if request.method == "POST" and 'place_bid' in request.POST:
        product_id = request.POST["product"]
        user = request.POST["user"]
        newbid = int(request.POST["bid"])

        product = Listing.objects.get(id=product_id)
        bidder = User.objects.get(username= user)
        oldbid = int(Bid.objects.get(listing=product).amount)

        if oldbid >= newbid:
            message = f'Your bid must be greater than the existing bid'
            return render(request, 'auctions/view_listing.html', {'product': product, 'comments':comments, 'message':message, 'list_creator':list_creator, 'highest_bidder':highest_bidder})
        else:
            bidobj = Bid.objects.get(listing=product)
            bidobj.amount = newbid
            bidobj.bidder = bidder
            product.price= bidobj.amount
            product.save()
            message = 'Your bid is the current bid'
            return render(request, 'auctions/view_listing.html', {'product': product, 'comments':comments, 'message':message, 'newbid':newbid, 'highest_bidder':highest_bidder})

    if request.method == "POST" and 'close' in request.POST:
        product_id = request.POST["product"]
        product=Listing.objects.get(pk=product_id)
        product.status = False
        product.save()

    if request.method == "POST" and 'submit_comment' in request.POST:
        comment_text= request.POST['comment']
        commenter_id = request.POST['user']
        product_id  = request.POST['product']
        commenter=User.objects.get(pk=commenter_id)
        product=Listing.objects.get(pk=product_id)
        Comment_on_listing(comment_text=comment_text, listing=product, commenter=commenter).save()
        
        

    if product:
        return render(request, 'auctions/view_listing.html', {'product': product, 'comments':comments, 'list_creator':list_creator, 'highest_bidder':highest_bidder})



def watchlist(request, username):
    user = User.objects.get(username=username)
    watched_items=user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {'watched_items': watched_items})


def categories(request):
    listings  = Listing.objects.values_list('category', flat=True).order_by()
    listings = [i for i in listings if i]
    for listing in listings:
        print(type(listing))
    return render(request, 'auctions/categories.html', {'listings': listings})

def individual_cat(request, individual_cat):
    matching_cats = Listing.objects.filter(category=individual_cat)

    return render(request, 'auctions/individual_cats.html', {'products':matching_cats, 'category':individual_cat})