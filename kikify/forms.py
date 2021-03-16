from django import forms
from django.contrib.auth.models import User
from kikify.models import UserProfileInfo, RecordLabel


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfileInfo
        exclude = ('user',)


class RecordLabelForm(forms.ModelForm):
    picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True)

    class Meta:
        model = RecordLabel
        exclude = ('user',)
