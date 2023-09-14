from django import forms
from django.contrib.auth.models import User

class sign(forms.Form):
    first_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your First Name'}))
    last_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Last Name'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-contorl','placeholder':'Enter Your Password'}))
    Confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Confirm Password'}))

    def clean(self):
        x=super().clean()
        if x['password'] != x['Confirm_password']:
            raise forms.ValidationError('Password Dose Not Match')
        if User.objects.filter(email = x['email']).exists():
            raise forms.ValidationError("Your Email Are Already Exists")
        if User.objects.filter(username = x['username']).exists():
            raise forms.ValidationError('Your Username Is Already Exists')
        