from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'mechanix'

urlpatterns = [

	path('', views.welcome, name="welcome"),

    path('login/', auth_views.LoginView.as_view(
        template_name='Login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('signup/', views.signup_view, name='signup'),

    path('logout/', auth_views.LogoutView.as_view(next_page='mechanix:welcome'), name='logout'),

    path('troubleshoot/', views.troubleshoot, name="troubleshoot"),

    path('find-shop/', views.findShop, name="find_shop"),

    path('discussion/', views.discussion, name="discussion"),

    path('discussion/edit/<int:post_id>/', views.edit_post, name='edit_post'),

    path('discussion/delete/<int:post_id>/', views.delete_post, name='delete_post'),

]
