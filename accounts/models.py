from django.db import models
from parler.models import TranslatableModel , TranslatedFields 
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from blog.models import ArchiveMonth , ArchiveYear
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


# Create your models here.

class Category(models.Model):
    ROLES = [
        ('owner' , 'مدیر کل'),
        ('programmer' , 'پشتیبانی برنامه نویسی'),
        ('graphic' , 'پشتیبانی گرافیک'),
        ('analyse' , 'پشتیبانی تحلیل داده'),
        ('moshavere' , 'پشتیبانی مشاوره'),
   
    ]
    category = models.CharField(_('category'),max_length=255 , choices=ROLES)

    def __str__(self):
        return self.category


class CustomUser(AbstractUser):
    ROLES = [
        ('modir' , 'modir'),
        ('ozv mamoli' , 'ozv mamoli'),
    ]

    phone_number = models.PositiveIntegerField(null=True , blank=True)
    image = models.ImageField(verbose_name = 'profile' , upload_to ='user/profile/' , blank=True )
    roles = models.CharField(max_length=50 , choices=ROLES , verbose_name='نقش' , blank=True , default=ROLES[1][0] )
    category = models.ForeignKey(Category , on_delete=models.CASCADE , blank=True , null=True)

    def __str__(self):
        return self.username


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    view = models.BooleanField(null=True , blank=True , default=False)
    answered = models.BooleanField(null=True , blank=True , default=False)
    answer = models.TextField(null=True , blank=True , default=None)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomerComments(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("name") , max_length=255),
        body=models.TextField(_("body"))
    )

    def __str__(self):
        return self.name


class CategoryPost(TranslatableModel):
    translations = TranslatedFields(
    name = models.CharField(_("category_post") , max_length=255)
    )

    def __str__(self):
        return self.name


class TicketsCategory(models.Model):
    name = models.CharField(_('category'),max_length=255)


    def __str__(self):
        return self.name



class Tickets(models.Model):

    STATES = [
        ('closed' , 'بسته شده'),
        ('open' , 'باز'),
    ]

    title = models.CharField(_('title'),max_length=255)
    category = models.ForeignKey(TicketsCategory , on_delete=models.CASCADE)
    content = RichTextField(_('content'))
    order = models.BooleanField(default=False , null=True , blank=True)
    created = models.DateTimeField(auto_now=True , null=True , blank=True)
    view = models.BooleanField(default=True , null=True , blank=True)
    view_admin = models.BooleanField(default=False , null=True , blank=True)
    file = models.FileField(upload_to='files/' , null=True , blank=True , verbose_name='فایل')
    state = models.BooleanField(default=True , blank=True , null=True)
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE , default=None)


    def __str__(self):
        return self.title

class TicketComments (models.Model):
    user = models.TextField(null=True)
    support = models.TextField(null=True)
    ticket = models.ForeignKey(Tickets , on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket.title


class Post(TranslatableModel):
    translations = TranslatedFields(
        title= models.CharField(_('title') , max_length=250),
        content = RichTextField(_('body')),
        image = models.ImageField(upload_to='covers/'),
    )
    
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(CategoryPost , on_delete=models.CASCADE)
    view = models.IntegerField(null=True , blank=True , default =0)
    month = models.ForeignKey(ArchiveMonth , on_delete=models.CASCADE , null=True , blank=True)


    def __str__(self):
        return self.title



