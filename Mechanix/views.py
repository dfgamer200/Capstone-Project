from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DiscussionPost, Vote, Post, Shop
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponseRedirect
import json


# Create your views here.

def welcome(request):
	return render(request, "Welcome.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('mechanix:welcome')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'Login.html')

def logout_view(request):
        logout(request)
        return redirect('mechanix:welcome')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('mechanix:welcome')
        else:
            messages.error(request, "There was a problem with your signup. Please check the details.")
    else:
        form = UserCreationForm()

    return render(request, 'Signup.html', {'form': form})


def findShop(request):
    shops = Shop.objects.all()
    shops_json = json.dumps([
        {
            "name": s.name,
            "address": s.address,
            "latitude": s.latitude,
            "longitude": s.longitude,
        }
        for s in shops
    ])
    return render(request, "FindAShop.html", {"shops_json": shops_json})

@login_required(login_url='mechanix:login')
def discussion(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            DiscussionPost.objects.create(user=request.user, content=content)
            return redirect('mechanix:discussion')

    posts = DiscussionPost.objects.all().order_by('-created_at')
    return render(request, 'Discussion.html', {'posts': posts})


@login_required(login_url='mechanix:login')
def edit_post(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id, user=request.user)

    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content:
            post.content = new_content
            post.save()
            messages.success(request, "Post updated successfully.")
            return redirect('mechanix:discussion')

    return render(request, 'edit_post.html', {'post': post})


@login_required(login_url='mechanix:login')
def delete_post(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id, user=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('mechanix:discussion')

    return render(request, 'confirm_delete.html', {'post': post})

def troubleshoot(request):
	return render(request, "Troubleshoot.html")

@login_required
def vote_view(request, post_id, vote_type):
    post = get_object_or_404(Post, id=post_id)

    # Determine vote value (+1 for upvote, -1 for downvote)
    value = 1 if vote_type == "upvote" else -1

    # Check if the user already voted
    existing_vote = Vote.objects.filter(user=request.user, post=post).first()

    if existing_vote:
        if existing_vote.value == value:
            existing_vote.delete()  # Clicking same arrow again removes the vote
        else:
            existing_vote.value = value  # Change upvote ↔ downvote
            existing_vote.save()
    else:
        Vote.objects.create(user=request.user, post=post, value=value)

    # Redirect back to the discussion page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def find_shop_view(request):
    shops = list(Shop.objects.values('name', 'latitude', 'longitude', 'address'))
    return render(request, 'find_shop.html', {'shops': shops})