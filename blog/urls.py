from unicodedata import name
from django.urls import path , include

from .views import *

urlpatterns = [
    path('blog/' , blog_main , name='blogmain'),
    path('blog/archieves/<slug:month>/<int:year>' ,archieve_search , name='archive_search' ),
    path('blog/details/<int:id>' , details_post , name='details')
    # path('blog/new_post/' , new_post , name='newpost'),

]
