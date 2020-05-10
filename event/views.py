from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Profile,Event,Venue
import json
from mpesa_api.core.mpesa import Mpesa
import requests
from django.views.decorators.csrf import csrf_exempt
from .mpesa import *
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse, JsonResponse


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

def venues(request):
    venues = Venue.objects.all()
    return render(request,"venues.html",{"venues":venues})

def viewVenue(request,pk):
    venue = Venue.objects.get(id=pk)
    return render(request,"venue-details.html",{"venue":venue})

def getAccessToken(request):
    consumer_key = 'wWXruSHVkm5ye7R2sVCFQ08zv7wNdc2q'
    consumer_secret = 'IWI63auaCuzIJIZY'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def sanitiseNumber(phone):
    string_number = str(phone)
    if string_number.startswith("7"):
        string_number="254"+string_number
        # print(string_number)
        # print("KO")
        return int(string_number)
    return phone




def buyTicket(request,pk):
    event = Event.objects.get(id=pk)
    # print(user.profile.phoneNumber)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": event.ticketFee,
        "PartyA": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "CallBackURL": "http://d22c1918.ngrok.io/confirmation/",
        "AccountReference": str(event.name),
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)  
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


def bookVenue(request,pk):
    venue = Venue.objects.get(id=pk)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": venue.price,
        "PartyA": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": sanitiseNumber(request.user.profile.phone_number),  # replace with your phone number to get stk push
        "CallBackURL": "http://d22c1918.ngrok.io/confirmation/",
        "AccountReference": str(venue.name),
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)  
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
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "http://d22c1918.ngrok.io/confirmation/",
               "ValidationURL": "http://d22c1918.ngrok.io/validation"}
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
    print(mpesa_payment) 
    if mpesa_payment['Body']['stkCallback']['ResultCode']==0:
        mpesa_payment = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item']
        print(mpesa_payment)
        #save payment here
        print("confirmed payment")
        context = {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context))    
