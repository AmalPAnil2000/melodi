# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class SocialLinksForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['facebook_url', 'linkedin_url', 'twitter_url', 'instagram_url']
        widgets = {
            'facebook_url': forms.URLInput(attrs={'placeholder': 'Facebook URL'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'LinkedIn URL'}),
            'twitter_url': forms.URLInput(attrs={'placeholder': 'Twitter URL'}),
            'instagram_url': forms.URLInput(attrs={'placeholder': 'Instagram URL'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'music_file','cover_image', 'category']
