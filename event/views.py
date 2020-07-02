from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Profile,Event,Venue,Organisation,Cart,Tickets,Transactions
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

def addToCart(request,pk):
    event = Event.objects.get(id=pk)
    cart = Cart(user=request.user,event=event)
    cart.save()
    return redirect("/view-cart")

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

def getAccessToken():
    consumer_key = 'YR6ZT25vHEXOhwBpjOaXOemjE88PGGQp'
    consumer_secret = 'kwMf8UX2hAgEljk5'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    print(mpesa_access_token)
    return validated_mpesa_access_token

def sanitiseNumber(phone):
    string_number = str(phone)
    if string_number.startswith("7"):
        string_number="254"+string_number
        return int(string_number)
    return phone

def lipa_na_mpesa_online(request,pk):
    event = Event.objects.get(id=pk)
    checkout_ticket(request,event)
    access_token = getAccessToken()
    print(sanitiseNumber(request.user.profile.phone_number))
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    stkPushrequest = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": event.ticketFee,
        "PartyA": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code, #587568
        "PhoneNumber": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "CallBackURL": "https://chainchain.herokuapp.com/confirmation/",
        "AccountReference": str(request.user.username),
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=stkPushrequest, headers=headers)
    print("statuscode: "+str(response.status_code))
    if response.status_code==200:
        data = response.json()
        if 'ResponseCode' in data.keys():
            if data['ResponseCode']==0:
                merchant_id = data['MerchantRequestID']
        pass
    merchant_id = response
    print(response.json())
    return redirect("/")

@csrf_exempt
def register_urls(request):
    access_token = getAccessToken()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://chainchain.herokuapp.com//confirmation/",
               "ValidationURL": "https://chainchain.herokuapp.com/validation/"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)
@csrf_exempt
def call_back(request):
    pass
@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
@csrf_exempt
def confirmation(request):
    print("called")
    mpesa_body =request.body.decode('utf-8')
    print(mpesa_body)
    try:
        mpesa_payment = json.loads(mpesa_body)
        print(mpesa_payment)
    except Exception as e:
        print(e)
        context = {
            "ResultCode": 1,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context))
    # print(mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'])
    if mpesa_payment['Body']['stkCallback']['ResultCode']==0:
        print(request.user)
        transaction = Transactions(
           phone = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value'],
           amount = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'],
           MpesaReceipt = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
           checkoutRequestId = mpesa_payment['Body']['stkCallback']['CheckoutRequestID'],
           status = "Success",
           direction="in"
       )
        transaction.save()
        return redirect("/")
    transaction = Transactions(status=mpesa_payment['Body']['stkCallback']['ResultDesc'])
    print("failed")
    return redirect("/")

def cart_checkout(request):
    total=0
    items = Cart.objects.filter(user=request.user)
    for item in items:
        total = total+item.event.ticketFee
    access_token = getAccessToken()
    print(sanitiseNumber(request.user.profile.phone_number))
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    stkPushrequest = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": total,
        "PartyA": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code, #587568
        "PhoneNumber": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "CallBackURL": "https://chainchain.herokuapp.com/confirmation/",
        "AccountReference": str(request.user.username),
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=stkPushrequest, headers=headers)
    print("statuscode: "+str(response.status_code))
    if response.status_code==200:
        data = response.json()
        if 'ResponseCode' in data.keys():
            if data['ResponseCode']==0:
                merchant_id = data['MerchantRequestID']
        pass
    merchant_id = response
    print(response.json())
    return redirect("/")