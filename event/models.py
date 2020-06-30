from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    dp =  models.ImageField(upload_to='images')
    bio = models.CharField(max_length=500)
    phone_number = models.BigIntegerField(null=True)
    
    
    def save_profile(self):
        return self.save()

    def delete_profile(self):
        return self.delete()
    
    def __str__(self):
        return self.user.username

class Organisation(models.Model):
    admin = models.ForeignKey(User,on_delete=models.CASCADE,related_name='organisation')
    logo =  models.ImageField(upload_to='images/logos')
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    paybill = models.BigIntegerField()
    
    def save_organisation(self):
        return self.save()

    def delete_organisation(self):
        return self.delete()
    
    def __str__(self):
        return self.name

class Venue(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='venue')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='venues')
    location = models.CharField(max_length=50)
    images1 = models.ImageField(upload_to='images')
    images2 = models.ImageField(upload_to='images')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.BigIntegerField()
    paybillNumber = models.BigIntegerField()
    
    def __str__(self):
        return self.organisation.name
    
    def saveVenue(self):
        return self.save()
    
    def deleteVenue(self):
        return self.delete()

class statusVenue(models.Model):
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE,related_name='status')
    start = models.DateTimeField()
    stop = models.DateTimeField()
    time = models.CharField(max_length=100)
    booked = models.BooleanField(default=True)

    def __str__(self):
        return self.venue.name

class Event(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='events')
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='events')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400,default="no description")
    poster = models.ImageField(upload_to='images',blank=True)
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE,related_name='event')
    statusVenue = models.ForeignKey(statusVenue,on_delete=models.CASCADE,related_name="event")
    dressCode = models.CharField(max_length=200)
    ticketFee = models.BigIntegerField()
    tickets = models.BigIntegerField()
    paybillNumber = models.BigIntegerField()
    GOH = models.CharField(max_length=20)
    MC = models.CharField(max_length=20)
    Date = models.DateTimeField()

    

    def __str__(self):
        return self.user.username

    def saveEvent(self):
        return self.save()

class Posters(models.Model):
    poster = models.ImageField(upload_to='images',blank=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='events_poster')

    def __str__(self):
        return self.event

    def saveEvent(self):
        return self.save()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
# M-pesa Payment models
class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    merchant_id = models.TextField(null=False,default="")
    checkout_request_id=models.TextField(null=False,default="")
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'

class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField() 
    merchant_id = models.TextField(null=False,default="")
    checkout_request_id=models.TextField(null=False,default="")
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'

class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
    def __str__(self):
        return self.first_name     


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart')
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='event_cart')

    def __str__(self):
        return self.user.username    
    
    def remove(self):
        return self.delete()

class Tickets(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tickets')
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='event_ticket')
    ticketNumber = models.CharField(max_length=30)
    active = models.CharField(max_length=5,default="true")


    def __str__(self):
        return self.user.username    