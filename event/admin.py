from django.contrib import admin
from .models import Profile,Organisation,Venue,statusVenue,Event,Cart
# Register your models here.

admin.site.register(Profile)
admin.site.register(Organisation)
admin.site.register(Venue)
admin.site.register(statusVenue)
admin.site.register(Event)
admin.site.register(Cart)