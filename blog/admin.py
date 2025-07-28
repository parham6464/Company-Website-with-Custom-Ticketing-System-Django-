from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import ArchiveMonth ,ArchiveYear
# Register your models here.
admin.site.register(ArchiveYear , TranslatableAdmin)
admin.site.register(ArchiveMonth , TranslatableAdmin)