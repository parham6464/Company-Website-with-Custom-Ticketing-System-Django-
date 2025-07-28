from django.urls import path , include

from .views import *

urlpatterns = [
    path('home/' , show_home , name='home'),
]