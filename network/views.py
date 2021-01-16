import json
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post
from .forms import NewPost


@csrf_exempt
def index(request):
    if request.method == 'POST':
        content = request.POST['content']
        addpost = Post(poster=request.user, content=content)
        addpost.save()

    posts = Post.objects.all().order_by('date_time').reverse()
    paginated = Paginator(posts, 10)
    currentpage = request.GET.get('page')
    try:
        paginated = paginated.page(currentpage)
        nextpage = int(currentpage)+1
        previouspage = int(currentpage)-1
        hasnext = paginated.has_next()
        hasprevious = paginated.has_previous()

    except PageNotAnInteger:
        paginated = paginated.page(1)
        nextpage = 2
        previouspage = 0
        hasnext = paginated.has_next()
        hasprevious = paginated.has_previous()

    context = {
        'posts': paginated,
        'nextpage': nextpage,
        'previouspage': previouspage,
        'hasnext': hasnext,
        'hasprevious': hasprevious,
    }

    return render(request, "network/index.html", context)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def profile_page(request, profile_name):
    if request.method == "PUT":
        data = json.loads(request.body)
        value = data['value']
        profile_id = data['id']

        viewed_profile = User.objects.get(id=profile_id)
        num_followers = viewed_profile.followers.all().count()
        datadict = {
            'num_followers': num_followers
        }
        if value == 'Follow':
            viewed_profile.followers.add(request.user)
        elif value == 'Unfollow':
            viewed_profile.followers.remove(request.user)
        return JsonResponse(datadict)

    try:
        requested_profile = User.objects.get(username=profile_name)
        follower_count = requested_profile.followers.count()
        following_count = requested_profile.following.count()
        user_posts = requested_profile.posts.all().order_by('date_time').reverse()
        is_loggedin_user = request.user.id != requested_profile.id
        is_following = request.user in requested_profile.followers.all()

        paginated = Paginator(user_posts, 10)
        currentpage = request.GET.get('page')
        try:
            paginated = paginated.page(currentpage)
            nextpage = int(currentpage)+1
            previouspage = int(currentpage)-1
            hasnext = paginated.has_next()
            hasprevious = paginated.has_previous()

        except PageNotAnInteger:
            paginated = paginated.page(1)
            nextpage = 2
            previouspage = 0
            hasnext = paginated.has_next()
            hasprevious = paginated.has_previous()

        context_dict = {
            'requested_profile': requested_profile,
            'follower_count': follower_count,
            'following_count': following_count,
            'user_posts': paginated,
            'is_loggedin_user': is_loggedin_user,
            'nextpage': nextpage,
            'previouspage': previouspage,
            'hasprevious': hasprevious,
            'hasnext': hasnext,
            'is_following': is_following
        }
        return render(request, "network/profile.html", context_dict)
    except:
        return render(request, "network/profile.html", {'message': f'Error! No such user as {profile_name}'})


@login_required
def following(request):
    userfollowing = request.user.following.all()
    posts = Post.objects.all()

    following_posts = []
    for post in posts:
        if post.poster in userfollowing:
            following_posts.append(post)
    following_posts = sorted(
        following_posts, key=lambda post: post.date_time, reverse=True)

    paginated = Paginator(following_posts, 10)
    currentpage = request.GET.get('page')
    try:
        paginated = paginated.page(currentpage)
        nextpage = int(currentpage)+1
        previouspage = int(currentpage)-1
        hasnext = paginated.has_next()
        hasprevious = paginated.has_previous()

    except PageNotAnInteger:
        paginated = paginated.page(1)
        nextpage = 2
        previouspage = 0
        hasnext = paginated.has_next()
        hasprevious = paginated.has_previous()
    # following_posts = userfollowing.intersection(posts)

    # following_posts = following_posts.order_by('date_time').reverse()

    context = {
        'posts': paginated,
        'nextpage': nextpage,
        'previouspage': previouspage,
        'hasnext': hasnext,
        'hasprevious': hasprevious
    }
    return render(request, "network/index.html", context)


@csrf_exempt
def edit_post(request, postid):
    if request.method == 'PUT':
        data = request.body.decode()
        data = json.loads(data)
        new_content = data.get('content')
        post_id = data.get('id')
        post_to_edit = Post.objects.get(id=post_id)
        post_likes = post_to_edit.liker.all().count()
        post_owner = post_to_edit.poster
        post_to_edit.content = new_content
        post_to_edit.save()
        datadict = {"post_content": post_to_edit.content, "post_poster": post_owner.username, 'post_id': post_to_edit.id,
                    "post_date_time": post_to_edit.date_time.strftime("%b %d %Y, %I:%M %p"), "post_likes": post_likes}

        # dataJSON = json.dumps(datadict)

        # return HttpResponse(status=204)
        return JsonResponse(datadict)
    else:
        return HttpResponse("NOT ALLOWED")

    # post_to_edit = Post.objects.get(id=postid)
    # post_owner = post_to_edit.poster
    # post_content = post_to_edit.content
    # if request.method == 'PUT':
    #     edit_content = request.POST['content']
    #     post_to_edit.content = edit_content
    #     post_to_edit.save()
    #     new_content = post_to_edit.content
    #     return HttpResponse(f"{post_content} <br> {new_content}")

    # if request.user == post_owner:
    #     context = {
    #         'post_content': post_content
    #     }
    #     return render(request, "network/editpost.html", context)
    # else:
    #     return HttpResponse("<h1>You do not own this post<h1>")


@csrf_exempt
def like_post(request, postid):
    if request.method == 'PUT':
        data = request.body.decode()
        data = json.loads(data)
        todo = data.get('todo')
        postid = data.get('postid')
        post_to_like = Post.objects.get(id=postid)
        if todo == 'like':
            post_to_like.liker.add(request.user)
            post_to_like.save()
        elif todo == 'unlike':
            post_to_like.liker.remove(request.user)
            post_to_like.save()
        likes_count = post_to_like.liker.all().count()
        datadict = {
            'likes_count': likes_count
        }
        return JsonResponse(datadict)
    else:
        return HttpResponse('NOT ALLOWED')
