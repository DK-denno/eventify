from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name="home"),
    path('profile/', views.profile,name="profile"),
    path('event/<int:pk>/', views.event,name="event"),
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('stkpush/<int:pk>/', views.buyTicket, name='lipa_na_mpesa'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('validation/', views.validation, name='validation'),
    path('register_urls/', views.register_urls, name='register_urls'),
    path("venues/",views.venues,name="venues"),
    path("venues/<int:pk>/",views.viewVenue,name="viewVenue"),
    path("bookVenue/<int:pk>/",views.bookVenue,name="book-venue")
    
]


