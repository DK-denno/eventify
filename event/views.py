from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Profile,Event,Venue,Organisation,Cart,Tickets
from .forms import ProfileForm,EventForm
import json
from mpesa_api.core.mpesa import Mpesa
import requests
from django.views.decorators.csrf import csrf_exempt
from .mpesa import *
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse, JsonResponse
import random
import string


# Create your views here.


@login_required
def index(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = Profile(user=request.user)
        profile.save()
    events = Event.objects.all()
    return render(request,'index.html',{"events":events})

@login_required
def profile(request):
    if request.method == 'POST':
        profForm = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        eventForm = EventForm(request.POST,request.FILES)
        if profForm.is_valid():
            profForm.save()
            return redirect('profile')
        if eventForm.is_valid():
            eventForm.save()
            return redirect('profile')
    profForm = ProfileForm()
    eventForm = EventForm()
    venues = Venue.objects.filter(user=request.user)
    events = Event.objects.filter(user=request.user)
    return render(request,'profile/profile.html',{"prof":profForm,"venues":venues,"eventForm":eventForm,"events":events})
        

@login_required
def event(request,pk):
    event = Event.objects.get(id=pk)
    return render(request,"event.html",{"event":event})

def venues(request):
    venues = Venue.objects.all()
    return render(request,"venues.html",{"venues":venues})

def viewVenue(request,pk):
    venue = Venue.objects.get(id=pk)
    return render(request,"venue-details.html",{"venue":venue})

def buyTicket(request,pk):
    event = Event.objects.get(id=pk)
    cart = Cart(user=request.user,event=event)
    cart.save()
    return redirect("/")

def viewCart(request):
    total=0
    items = Cart.objects.filter(user=request.user)
    for item in items:
        total = total+item.event.ticketFee
    return render(request,"cart.html",{"items":items,"total":total})

def removeCart(request,pk):
    item = Cart.objects.get(id=pk)
    item.remove()
    return redirect("/view-cart")

def testEmail(request):
    return render(request,"email/email.html",{})



def checkout_ticket(request,event):
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    unique_id = ''.join(random.choice(allowed_chars) for _ in range(32))
    ticket = Tickets(user=request.user,event=event,ticketNumber=unique_id)
    ticket.save()
    return ticket