from django.urls import path
from . import views

urlpatterns = [

	path('', views.welcome, name="welcome"),
    path('login/', views.login, name="login"),
    path('troubleshoot/', views.troubleshoot, name="troubleshoot"),
    path('find-shop/', views.findShop, name="find_shop"),
    path('discussion/', views.discussion, name="discussion"),
]
