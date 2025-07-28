from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy
# Create your views here.

from django.shortcuts import render 
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render ,redirect 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login , logout 
from django.contrib import messages
from django.views.generic import ListView , DeleteView , DetailView , CreateView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import *

# Create your views here.

def services_page(request):
    return render (request , 'services.html')

def portfolio_page(request):
    return render (request , 'portfolio.html')

def contact_page(request):
    if request.method == "POST":
        print('1')
        if request.POST['name'] !='' or request.POST['email'] !='' or request.POST['subject'] !='' or request.POST['message']!='':
            if "@" in request.POST['email']:
                Contact.objects.create(name=request.POST['name'] , email=request.POST['email'] , subject = request.POST['subject'] , body=request.POST['message'])
                messages.success(request , 'your message sent')
            else:
                messages.warning(request , 'email is not valid')
        else:
            messages.warning(request , 'fill all the parameters')
    return render(request, 'contact.html')



def about_us(request):
    return render(request , 'about.html')