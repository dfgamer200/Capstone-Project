from django.shortcuts import render

# Create your views here.

def welcome(request):
	return render(request, "Welcome.html")

def login(request):
	return render(request, "Login.html")

def findShop(request):
	return render(request, "FindAShop/.html")

def discussion(request):
	return render(request, "Discussion/.html")

def troubleshoot(request):
	return render(request, "Troubleshoot/.html")
