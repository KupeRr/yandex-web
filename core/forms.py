from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserForm(UserCreationForm):
    password1 = forms.CharField(initial='1',widget = forms.TextInput(
        attrs={'class':'form-control','type':'password', 'name':'password', 'readonly': True}), 
        label="Пароль")
    password2 = None