from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DiscussionPost
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

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
	return render(request, "FindAShop.html")

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
