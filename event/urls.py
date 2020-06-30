from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name="home"),
    path('profile/', views.profile,name="profile"),
    path('event/<int:pk>/', views.event,name="event"),
    path('buyTicket/<int:pk>/', views.buyTicket, name='lipa_na_mpesa'),
    path("venues/",views.venues,name="venues"),
    path("venues/<int:pk>/",views.viewVenue,name="viewVenue"),
    path("view-cart/",views.viewCart,name="view-cart"),    
    path("remove-cart/<int:pk>/",views.removeCart,name="remove-cart"),
    path("testEmail",views.testEmail,name="testEmail"),    
    
]


