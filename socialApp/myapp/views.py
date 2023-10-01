import os
from django.http import request
from django.shortcuts import  render,HttpResponse, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    num = 0
    all_posts = Post.objects.all().order_by('-date_created')
    allComm = Comment.objects.all()
    allusr = User.objects.all().order_by('username')
    param = {"posts": all_posts, "comments": allComm, "users": allusr}
    return  render(request, 'index.html', param)

def handleSignup(request):
    if request.method == 'POST':
        # Getting all parameters
        uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(uname, lname, fname, email, password)

        # creating user in databse
        myuser = User.objects.create_user(username=uname, email=email, password=password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        print('User succesful created')
    else:
        return HttpResponse('Not Allowed')
    return redirect('/')

def handleLogin(request):
    if request.method == 'POST':
        # Getting all parameters
        loginUname = request.POST.get('unamelogin')
        loginPassword = request.POST.get('passwordlogin')
        user = authenticate(username=loginUname, password=loginPassword)

        if user is not None:
            print('success')
            login(request, user)
        else:
            return HttpResponse('Invalid try again')
        return redirect('/')
    else:
        return HttpResponse('404 not found')

def handleLogout(request):
    logout(request)
    return render(request, 'index.html')

@login_required
def createPost(request):
    if request.method == 'POST':
        content_text = request.POST.get('contentText')
        content_img = request.POST.get('image')
        # print(content_img, content_text)
        try:
            post = Post.objects.create(creater=request.user, content_text=content_text, content_image=content_img)
            print('Succesful posted')
            return HttpResponseRedirect(reverse('index'))
        except Exception as e:
            return HttpResponse(e)
    return HttpResponse("success Post")

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(creater=user).order_by('-date_created')
    is_posts = False
    if (posts.count() > 0):
        is_posts = True
    follow = Follower.objects.all()
    if user not in follow:
        (follower, create) = Follower.objects.get_or_create(user=user)
        follower.save()
    allComm = Comment.objects.all()
    Follower.objects.get(user=user).followers.all()
    follow = Follower.objects.get(user=user).followers.all()
    followCount = follow.count()
    if request.user in Follower.objects.get(user=user).followers.all():
        follower = True
    else:
        follower = False
    param = {"post": posts, "user": user, "comments": allComm, "is_follower": follower, "follCount": followCount, "is_post": is_posts}
    return render(request, 'profile.html', param)

@login_required
def addComment(request, post_id):
    if request.method == 'POST':
        commtext = request.POST.get('comment')
        post = Post.objects.get(id=post_id)
        try:
            newcomm = Comment.objects.create(post=post, commenter=request.user, comment_content=commtext)
            post.comment_count += 1
            post.save()
            newcomm.save()
        except Exception as e:
            return HttpResponse(e)

    return HttpResponseRedirect(reverse('index'))

@login_required
def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    # for request.user in post.likers.all():
    if request.user in post.likers.all():
        post.likers.remove(request.user)
        if post.likers_count == 0:
            post.likers_count = 0
        else:
            post.likers_count -= 1
        post.save()
    else:
        post.likers_count += 1
        post.likers.add(request.user)
        post.save()
    return HttpResponseRedirect(reverse('index'))

@login_required
def follow(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = User.objects.get(username=username)
            (follower, create) = Follower.objects.get_or_create(user=user)
            follower.followers.add(request.user)
            follower.save()
    else:
        print("not auth")
    return redirect('/'+username)\

@login_required
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = User.objects.get(username=username)
            follower = Follower.objects.get(user=user)
            follower.followers.remove(request.user)
            follower.save()
    else:
        print("not auth")
    return redirect('/'+username)

@login_required
def deleteComment(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user in post.commentors:
                post.commentors.remove(request.user)
    else:
        print('not auth')

@login_required
def editComment(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user in post.commentors:
                post.commentors.editComment(request.user)
    else:
        print('not auth')
