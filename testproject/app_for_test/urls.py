from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('register/', views.registration_view, name='register'),
    path('verify_email_sent/', views.verify_email_sent, name='verify_email_sent'),
    path('verify_email/<str:verification_key>/', views.verify_email_confirm, name='verify_email_confirm'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]