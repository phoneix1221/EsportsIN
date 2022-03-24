from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core import validators
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError







class UserRegisterForm(UserCreationForm):
    username=forms.CharField(
         widget=forms.TextInput(attrs={'class':'form-control email_input', 'align':'center', 'placeholder':'Username'}),
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': "form-control email_input",'align':'center','placeholder':'email'}),
        )
    password1 = forms.CharField(
       
        widget=forms.PasswordInput(attrs={'class':'form-control email_input', 'type':'password', 'align':'center', 'placeholder':'password'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control email_input', 'type':'password', 'align':'center', 'placeholder':'Confirm password'}),
    )
   

    class Meta:
        model = User
        fields = ['username', 'email']
        


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image','phone_number','spoken_language']
        




class Myamount(forms.Form):
    amount = forms.IntegerField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'placeholder': 'Enter amount'})