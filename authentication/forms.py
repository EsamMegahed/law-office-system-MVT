from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserCreateForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['username','email','password1','password2']



class UserEditForm(forms.ModelForm):
    class Meta:
        model= User
        fields = ['username','email',]

class UserPasswordChangeForm(forms.Form):
    new_password = forms.CharField(label=_('New Password'),widget=forms.PasswordInput())
    confirm_password = forms.CharField(label=_('Confirm Password'),widget=forms.PasswordInput())