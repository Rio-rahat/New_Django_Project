from django import forms
from django.contrib.auth.models import User
from Login_app import models


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = models.userInfo
        fields = ('facebook_id', 'profile_pic')

