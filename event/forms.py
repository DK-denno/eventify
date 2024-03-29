from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Event

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2', ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ "dp","bio","phone_number" ]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','poster','dressCode','ticketFee','paybillNumber','GOH','MC','Date']