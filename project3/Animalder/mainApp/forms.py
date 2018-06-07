from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from mainApp.models import Profile

class SignUpForm(UserCreationForm):
    dateOfBirth = forms.DateField(help_text='Format: YYYY-MM-DD', label='Date of birth')
    profilePhoto = forms.ImageField(label='Profile photo')
    sex = forms.ChoiceField(choices=Profile.SEX)
    lookingFor = forms.ChoiceField(choices=Profile.SEX, label='Looking for')

    class Meta:
        model = User
        fields = ('username',
                    'first_name', 
                    'last_name', 
                    'email', 
                    'dateOfBirth', 
                    'sex', 
                    'lookingFor',
                    'profilePhoto', 
                    'password1', 
                    'password2')

class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='')