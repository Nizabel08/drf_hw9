from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('profile/', views.profile, name = 'profile'),
]

