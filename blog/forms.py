
from mimetypes import init
from django import forms 
from allauth.account.forms import LoginForm
from django.contrib.auth.forms import UserCreationForm , UserChangeForm 
from django.contrib.auth.forms import AuthenticationForm
from typing import Any
from django.contrib.auth import get_user_model
from accounts.models import Post




# class AddNewPostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = '__all__'


# class NewPostForm(forms.Form):
#     title = forms.CharField(max_length=255)