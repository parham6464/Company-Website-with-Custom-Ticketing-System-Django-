from django.urls import path , include

from .views import *

urlpatterns = [
    
    path('login/',login1 , name='login1'),
    path('sign-up/',sign_up , name='signup1'),
    path('logout/' , log_out , name='logout1'),
    path('profile/' ,profile, name='profile'),
    path('profile/tickets/' , all_tickets_user , name='all_tickets_user'),
    path('profile/services/fill/' , fill_services , name='fill_services'),
    path('profile/tickets/<int:id>/' , chat_ticket , name='chat'),
    path('profile/tickets/accepts_order/<int:id>/' , accept_order , name='accept_order'),
    path('profile/tickets/active_orders/' , active_orders , name='active_orders'),
    path('profile/tickets/complete_orders/' , done_orders , name='done_orders'),
    path('profile/tickets/order_admins/' ,ticket_orders_admins , name='ticket_orders_admins'),
    path('profile/tickets/order_admins_complete/' ,ticket_orders_admins_complete , name='ticket_orders_admins_complete'),
    path('profile/tickets/support_admin/' , ticket_support_admins_open , name='ticket_support_admins_open'),
    path('profile/tickets/support_admin_close/' , ticket_support_admins_closed , name='ticket_support_admins_closed'),
    path('profle/tickets/contacts/' , contact_open , name="contact_open"),
    path('profle/tickets/contacts/closed/' , contact_closed , name="contact_close"),
    path ('profile/tickets/contacts/<int:id>/' , chat_contact , name='chat_contact'),
    path('profile/open_ticket/' ,create_ticket , name='open_ticket'),
    path ('profile/save/file/<int:id>/' , save_file , name='save_file'),
    path('profile/tickets/open/<int:id>/' , open_ticket , name='open_ticket_admin'),
    path('profile/tickets/close/<int:id>/' , close_ticket , name='close_ticket_admin'),
    path('profile/changepassword/' , changepassword , name='changepassword'),
    path('login/forgetpassword/' , passwordforget , name='passwordforget'),
    path('login/complete/' , completereset , name='completereset'),
    path('profile/update/password/' , change_password_page , name='change_password_page'),
    path('profile/update/details/' , change_details_page , name='change_details_page'),

]
