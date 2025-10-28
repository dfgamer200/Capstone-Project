from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DiscussionPost
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.

def welcome(request):
	return render(request, "Welcome.html")

def login(request):
	return render(request, "Login.html")

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
