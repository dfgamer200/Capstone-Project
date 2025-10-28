from django.urls import path
from . import views

app_name = 'mechanix'

urlpatterns = [

	path('', views.welcome, name="welcome"),
    path('login/', views.login, name="login"),
    path('troubleshoot/', views.troubleshoot, name="troubleshoot"),
    path('find-shop/', views.findShop, name="find_shop"),
    path('discussion/', views.discussion, name="discussion"),
    path('discussion/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('discussion/delete/<int:post_id>/', views.delete_post, name='delete_post'),

]
