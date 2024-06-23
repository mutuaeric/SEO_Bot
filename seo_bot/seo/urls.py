from django.urls import path
from . import views

urlpatterns = [
    path('check-broken-links/', views.CheckBrokenLinks.as_view(), name='check_broken_links'),
   
]
