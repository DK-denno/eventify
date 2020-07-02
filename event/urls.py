from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name="home"),
    path('profile/', views.profile,name="profile"),
    path('event/<int:pk>/', views.event,name="event"),
    path('addToCart/<int:pk>/', views.addToCart, name='addToCart'),
    path('buyTicket/<int:pk>/', views.lipa_na_mpesa_online, name='buyTicket'),
    path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
    path("venues/",views.venues,name="venues"),
    path("venues/<int:pk>/",views.viewVenue,name="viewVenue"),
    path("view-cart/",views.viewCart,name="view-cart"),
    path("remove-cart/<int:pk>/",views.removeCart,name="remove-cart"),
    path("testEmail",views.testEmail,name="testEmail"),

]


