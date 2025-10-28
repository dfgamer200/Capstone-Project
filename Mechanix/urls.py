from django.urls import path
from . import views

urlpatterns = [

	path('', views.welcome, name="Welcome"),
    path('Login', views.login, name="Login"),
    path('Troubleshoot', views.troubleshoot, name="Troubleshoot"),
    path('FindAShop', views.findShop, name="FindAShop"),
    path('Discussion', views.discussion, name="Discussion"),
]
