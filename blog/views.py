# Create your views here.
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import FileResponse

# from .forms import AddNewPostForm

def blog_main(request):
    search_result = None
    if request.method == "POST":
        search_result = request.POST['title']


    ############## archives
    archives = ArchiveMonth.objects.all().order_by('-id')[:4]

    tmp = {}
    for i in archives:
        tmp[f'{i.month}'] = i.year.year 
    ######################################

    ############## post paginated
    posts = Post.objects.all()


    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)

    post_paginated = paginator.page(page)
    ###########################################
    most_viewed = Post.objects.all().order_by('-view')[:4]


    return render (request , 'blog/index.html' , {'archives':tmp , 'posts':post_paginated , "popular":most_viewed , 'search_result':search_result})


def archieve_search(request , month , year):
    search_result = None
    if request.method == "POST":
        search_result = request.POST['title']


    ############## archives
    archives = ArchiveMonth.objects.all().order_by('-id')[:4]

    tmp = {}
    for i in archives:
        tmp[f'{i.month}'] = i.year.year 
    ######################################

    ############## post paginated
    year_finder = ArchiveYear.objects.get(translations__year=year)
    archive_finder = ArchiveMonth.objects.get(translations__month=month , year=year_finder)

    posts = Post.objects.all().filter(month=archive_finder)


    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)

    post_paginated = paginator.page(page)
    ###########################################
    most_viewed = Post.objects.all().order_by('-view')[:4]


    return render (request , 'blog/index.html' , {'archives':tmp , 'posts':post_paginated , "popular":most_viewed , 'search_result':search_result})


#################################


def details_post(request , id):
    post =Post.objects.get(id=id)
    return render(request , 'blog/detail_post.html' , {'post':post})










##################################
# def new_post(request):
#     if request.method == "POST":
#         form=AddNewPostForm(request.POST)
#         if form.is_valid():
#             form.save()
    
#     return render(request , 'blog/newpost.html' , {"form":AddNewPostForm})