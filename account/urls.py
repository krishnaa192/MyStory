from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.loginUser, name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/', views.registerUser, name='register'),

    path('profile/<str:name>/', views.Profile, name='profile'),
    path('create-profile/', views.author_Profile, name='create-profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),

    path('portfolio/', views.add_portfolio, name='add-portfolio'),
    
    path('author/<str:name>/', views.AuthorProfile, name='author'),
]