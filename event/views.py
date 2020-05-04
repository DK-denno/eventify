from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.

@login_required
def index(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = Profile(user=request.user)
        profile.save()
    return render(request,'index.html')

@login_required
def profile(request):
    return render(request,'profile/profile.html')
