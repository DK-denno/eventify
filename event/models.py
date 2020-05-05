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
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    
    def save_organisation(self):
        return self.save()

    def delete_organisation(self):
        return self.delete()
    
    def __str__(self):
        return self.name

class Venue(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='venue')
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
    date = models.DateTimeField()
    time = models.CharField(max_length=100)
    booked = models.BooleanField(default=True)

    def __str__(self):
        return self.venue

class Event(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='events')
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='events')
    category = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='images',blank=True)
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE,related_name='event')
    dressCode = models.CharField(max_length=200)
    ticketFee = models.BigIntegerField()
    paybillNumber = models.BigIntegerField()
    GOH = models.CharField(max_length=20)
    MC = models.CharField(max_length=20)
    Date = models.DateTimeField()

    

    def __str__(self):
        return self.user.username

    def saveEvent(self):
        return self.save()