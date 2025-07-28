from django.shortcuts import render

# Create your views here.
from django.shortcuts import render 
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render ,redirect 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login , logout 
from allauth.account.forms import LoginForm 
from django.contrib import messages
from django.views.generic import ListView , DeleteView , DetailView , CreateView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import CustomerComments


def show_home(request):
    comments= CustomerComments.objects.all()
    for i in comments:
        print(i.name)
    return render(request,'index.html' , {"comments":comments})