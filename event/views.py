from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile,Event

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
    return render(request,'profile/profile.html')

@login_required
def event(request,pk):
    event = Event.objects.get(id=pk)
    return render(request,"event.html",{"event":event})