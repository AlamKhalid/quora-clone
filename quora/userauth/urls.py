from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from userauth.views import EditProfile

urlpatterns = [
    # Profile Section
    path('edit/', EditProfile, name="edit-profile"),
    path('about/', views.about, name='about'),
    path('<int:user_id>/', views.user_profile, name='user-profile'),

    # User Authentication
    path('sign-up/', views.sign_up, name="sign-up"),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
