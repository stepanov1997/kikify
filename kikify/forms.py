from django import forms
from django.contrib.auth.models import User
from kikify.models import UserProfileInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfileInfo
        exclude = ('user',)
