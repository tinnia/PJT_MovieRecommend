from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('users/', views.users, name='users'),
    path('getuserdetail/<str:user_name>/', views.getuserdetail, name='getUserDetail'),
    path('karma/<str:user_name>/', views.karma, name='karma'),
]
