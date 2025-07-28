from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import CustomUser , Post , CategoryPost , CustomerComments , Contact , TicketComments , Tickets , TicketsCategory  , TicketsCategory

from parler.admin import TranslatableAdmin

# Register your models here.





admin.site.register(CustomUser)
admin.site.register(Post , TranslatableAdmin)
admin.site.register(CategoryPost , TranslatableAdmin)
admin.site.register(CustomerComments , TranslatableAdmin)
admin.site.register(Contact )
admin.site.register(TicketComments )
admin.site.register(Tickets )
admin.site.register(TicketsCategory )