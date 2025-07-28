from django.urls import path , include

from .views import *

urlpatterns = [
    path('services/' , services_page , name='services'),
    path('portfolio/' , portfolio_page , name='portfolio' ),
    path('contact/' , contact_page , name='contact'),
    path('about-us/' , about_us , name='about_us')

]
