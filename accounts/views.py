from unicodedata import category
from django.shortcuts import render 
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render ,redirect 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login , logout 
from .models import Category, CustomUser, TicketComments, Tickets , Contact , TicketsCategory
from allauth.account.forms import LoginForm 
from django.contrib import messages
from django.views.generic import ListView , DeleteView , DetailView , CreateView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm , UserSignUpForm , ProfilePic1 , UpdateProfile , UpdatePasswordProfile , ForgetPassowrd , TicketForm , ChatForm , UploadFile
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def login1(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method =="POST":
        form = UserRegistrationForm(request.POST , )

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user1 = authenticate(request,username=username , password=password)
            if user1 is not None:
                login(request,user1)
                return redirect('profile')
            else:
                messages.warning(request,'نام کاربری یا رمز عبور شما اشتباه است')
                form = UserRegistrationForm()
                return render(request,"registration/login.html" , {'forms':form})
        else:
            messages.warning(request,'مقادیر را به درستی وارد کنید!')
            form = UserRegistrationForm()
            return render(request,"registration/login.html" , {'forms':form})

    else:
        form = UserRegistrationForm()
        return render(request,"registration/login.html" , {'forms':form})

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        password_checker = request.POST.get('password')
        if len(password_checker) < 8 :
            form = UserSignUpForm()
            messages.warning(request,'رمز عبور شما بسیار کوتاه است')
            return redirect("signup1")

        if len(request.POST.get('email'))== 0:
            form = UserSignUpForm()
            messages.warning(request,'باید ایمیل را وارد کنید')
            return redirect("signup1")
        if len(request.POST.get('phone_number')) == 0:
            form = UserSignUpForm()
            messages.warning(request,'لطفا شماره تلفن خود را وارد کنید')
            return redirect("signup1")
        if len(request.POST.get('username'))==0:
            form = UserSignUpForm()
            messages.warning(request,'لطفا نام کاربری را وارد کنید')
            return redirect("signup1")
        else:
            username = request.POST.get('username')
            check_user = CustomUser.objects.filter(username=username)
            if check_user == True:
                form = UserSignUpForm()
                messages.warning(request,'این نام کاربری توسط یه کاربر دیگر استفاده شده')
                return redirect("signup1")

        
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            CD = form.cleaned_data
            CustomUser.objects.create(username = CD['username'] , phone_number=CD['phone_number'] , password = make_password(CD['password']) , email=CD['email'])
            messages.success(request,'حساب شما با موفقیت ایجاد شد')
            return redirect("login1")
        else:
            form = UserSignUpForm()
            messages.warning(request,'هر ورودی را به درستی وارد کنید!')
            return redirect("signup1")
            

    else:
        form = UserSignUpForm()
    return render(request,"registration/signup.html",{'form':form})

@login_required
def log_out(request):
    if request.method =="POST":
        logout(request)
        return redirect('home')
    else:
        return render(request , 'logout.html')

@login_required
def changepassword(request):
    if request.method == "POST":
        new_pass = request.POST.get('new_pass')
        if len(new_pass)<8:
            messages.warning(request,'رمز عبور شما حداقل باید 8 کاراکتر باشد')
            return redirect('profile')
        else:
            my_user = CustomUser.objects.get(id=request.user.id)
            form = UpdatePasswordProfile(request.POST)
            if form.is_valid():
                CD = form.cleaned_data
                checker = check_password(CD['current_pass'] , my_user.password)
                if checker == True:
                    my_user.password = make_password(CD['new_pass'])
                    CustomUser.save(my_user)
                    messages.success(request,'رمز عبور شما با موفقیت تغییر کرد اکنون دوباره وارد شوید')
                    return redirect ('login1')
                else:
                    messages.warning(request,'رمز عبور شما با رمز عبور حساب شما برابر نیست')
                    return redirect ('profile')
                

    else:
        return render(request , 'Profile/index.html')


    

def passwordforget(request):
    if request.method == "POST":
        form = ForgetPassowrd(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                obj = CustomUser.objects.get(email=email)
                if obj.is_active == False:
                    messages.warning(request,'دسترسی اکانت شما بسته شده است')
                    form = ForgetPassowrd()
                    return render (request , 'registration/password_reset.html' , context={'form':form})

                send_list = []
                send_list.append(obj.email)
            except:
                messages.warning(request,'این ایمیل وجود ندارد')
                form = ForgetPassowrd()
                return render (request , 'registration/password_reset.html' , context={'form':form})

            try:
                send_mail(subject='اطلاعات حساب کاربری' , message=f'با عرض سلام و ادب رمز عبور شما در سایت انجمن علمی کامپیوتر در زیر نوشته شده است \n نا کاربری :\n {obj.username} \nرمز عبور :\n {obj.password}' , from_email=settings.EMAIL_HOST_USER ,recipient_list=send_list)
                return redirect('completereset')
            except:
                messages.warning(request,'ایمیل ارسال نشد')
                form = ForgetPassowrd()
                return render (request , 'registration/password_reset.html' , context={'form':form})

        else:
            messages.warning(request,'ایمیل را درست وارد کنید')
            form = ForgetPassowrd()
            return render (request , 'registration/password_reset.html' , context={'form':form})

            
    else:
        form = ForgetPassowrd()
        return render (request , 'registration/password_reset.html' , context={'form':form})

def completereset(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return render(request , '404.html')

    return render (request , 'registration/password_complete.html')

@login_required
def profile(request):
    active_orders=Tickets.objects.all().filter(order=True , state=True)
    all_tickets=Tickets.objects.all().filter(state=True)
    done_orders=Tickets.objects.all().filter(order=True , state=False)

    return render (request , 'profile/empty.html' , {"active_orders":active_orders , "all_tickets":all_tickets , "done_orders":done_orders})

@login_required
def all_tickets_user (request):

    ############## post paginated
    posts = Tickets.objects.all()


    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)

    all_tickets = paginator.page(page)
    ###########################################


    # all_tickets=Tickets.objects.all()
    return render (request , 'profile/ticket_lists.html' , {"tickets":all_tickets})

@login_required
def create_ticket(request):

    form = TicketForm()
    if request.method=="POST":
        form = TicketForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            TicketComments.objects.create(ticket = obj , user = obj.content , support=None)
            
            
    return render (request , 'profile/open_tickets.html' , {'form':form})

@login_required
def chat_ticket(request , id):
    

    if request.method == 'POST':
        form_chat = ChatForm(request.POST)
        if form_chat.is_valid():
            real_chat=form_chat.cleaned_data['Content']
            obj = Tickets.objects.get(id=id)
            if request.user != obj.user:
                TicketComments.objects.create(ticket=obj , user = None, support=real_chat)
                obj.view = False
                obj.save()
            else:
                TicketComments.objects.create(ticket=obj , user = real_chat, support=None)
                obj.view_admin = False
                obj.save()
    
    obj = Tickets.objects.get(id=id)
    if request.user.roles == 'modir':
        obj.view_admin = True
        obj.save()
    chats = TicketComments.objects.all().filter(ticket=obj)
    form_chat = ChatForm()

    return render (request , 'profile/chat.html' , {'ticket':obj , 'chats':chats , "ChatForm":form_chat})

@login_required
def accept_order(request , id):

    obj = Tickets.objects.get(id=id)
    obj.order = True
    obj.save()
    return redirect('chat' , id=id)

@login_required
def active_orders(request):

    ############## post paginated
    posts = Tickets.objects.all().filter(order=True , state=True)


    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)

    all_tickets = paginator.page(page)
    ###########################################


    # all_tickets=Tickets.objects.all().filter(order=True , state=True)
    return render (request , 'profile/order_tickets_user.html' , {"tickets":all_tickets})

@login_required
def done_orders(request):

    ############## post paginated
    posts = Tickets.objects.all().filter(order=True , state=False)


    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)

    all_tickets = paginator.page(page)
    ###########################################


    # all_tickets=Tickets.objects.all().filter(order=True , state=False)
    return render (request , 'profile/order_tickets_complete_user.html' , {"tickets":all_tickets})

#################### admins section
@login_required
def save_file(request , id):
    if request.user.roles == 'modir':
        if request.method=="POST":
            ticket = Tickets.objects.get(id=id)
            form = UploadFile(request.POST , request.FILES)
            if form.is_valid():
                obj=form.save(commit=False)
                ticket.file = obj.file 
                ticket.save()
    else:
        return HttpResponse('you dont have access')
    return redirect ('ticket_orders_admins')

@login_required
def ticket_orders_admins(request):

    if request.user.roles == 'modir':
        ############## post paginated
        posts = Tickets.objects.all().filter(order=True , state=True)


        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 10)

        all_tickets = paginator.page(page)
        ###########################################

        # all_tickets=Tickets.objects.all().filter(order=True , state=True)
        form = UploadFile()
        return render (request , 'profile/order_tickets.html' , {"tickets":all_tickets , 'form':form})
    else:
        return HttpResponse('you dont have access')


@login_required
def ticket_orders_admins_complete(request):
    if request.user.roles == 'modir':

        ############## post paginated
        posts = Tickets.objects.all().filter(order=True , state=False)


        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 10)

        all_tickets = paginator.page(page)
        ###########################################


        # all_tickets=Tickets.objects.all().filter(order=True , state=False)
        return render (request , 'profile/order_tickets.html' , {"tickets":all_tickets})
    else:
        return HttpResponse('you dont have access')

@login_required
def ticket_support_admins_open(request):
    if request.user.roles == 'modir':

        ############## post paginated
        posts = Tickets.objects.all().filter(order=False , state=True)


        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 10)

        all_tickets = paginator.page(page)
        ###########################################


        # all_tickets=Tickets.objects.all().filter(order=False , state=True)
        return render (request , 'profile/support_tickets.html' , {"tickets":all_tickets})
    else:
        return HttpResponse('you dont have access')

@login_required
def ticket_support_admins_closed(request):
    if request.user.roles == 'modir':

        ############## post paginated
        posts = Tickets.objects.all().filter(order=False , state=False)


        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 10)

        all_tickets = paginator.page(page)
        ###########################################


        # all_tickets=Tickets.objects.all().filter(order=False , state=False)
        return render (request , 'profile/support_tickets.html' , {"tickets":all_tickets})
    else:
        return HttpResponse('you dont have access')

@login_required
def close_ticket(request , id):
    if request.user.roles == 'modir':
        ticket = Tickets.objects.get(id=id)
        ticket.state = False
        ticket.save()
        return redirect ('ticket_orders_admins')
    else:
        return HttpResponse('you dont have access')

@login_required
def open_ticket(request , id):
    if request.user.roles == 'modir':
        ticket = Tickets.objects.get(id=id)
        ticket.state = True
        ticket.save()
        return redirect ('ticket_orders_admins')
    else:
        return HttpResponse('you dont have access')


############################ contact 
@login_required
def contact_open(request):
    if request.user.roles == 'modir':

        ############## post paginated
        posts = Contact.objects.all().filter(answered = False)


        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 10)

        all_tickets = paginator.page(page)
        ###########################################


        # all_tickets=Contact.objects.all().filter(answered = False)
        return render (request , 'profile/open_contact.html' , {"tickets":all_tickets})
    else:
        return HttpResponse('you dont have access')

@login_required
def contact_closed (request):
    if request.user.roles == 'modir':

        ############## post paginated
        posts = Contact.objects.all().filter(answered = True)


        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 10)

        all_tickets = paginator.page(page)
        ###########################################


        # all_tickets=Contact.objects.all().filter(answered = True)
        return render (request , 'profile/open_contact.html' , {"tickets":all_tickets})
    else:
        return HttpResponse('you dont have access')

@login_required
def chat_contact(request , id):
    if request.user.roles != 'modir':
        return HttpResponse('you dont have access')
        
    obj = Contact.objects.get(id=id)
    obj.view=True
    if request.method == 'POST':
        form_chat = ChatForm(request.POST)
        if form_chat.is_valid():
            real_chat=form_chat.cleaned_data['Content']
            tmp_list = []
            tmp_list.append(obj.email)
            send_mail(subject='پشتیبانی شرکت فلان' , message=f'{real_chat}' , from_email=settings.EMAIL_HOST_USER ,recipient_list=tmp_list)
            obj.answer = real_chat
            obj.answered = True
            obj.save()
    else:
        obj.save()
    
    form = ChatForm()

    return render(request , 'profile/chat_contact.html' , {"ticket":obj , 'ChatForm':form} )


##################################### services
@login_required
def fill_services (request):
    return redirect('open_ticket')


####################################### profile update and change password
@login_required
def change_password_page(request):
    if request.method=="POST":
        if request.POST['new_pass'] == '' or request.POST['repeat_pass'] == '' or request.POST['current_pass'] == '':
            messages.warning(request , 'همه ی فیلدها را پر کنید')
            return render (request ,'profile/change_password.html')
        new_pass = request.POST.get('new_pass')
        if len(new_pass) > 8:
            repeat_pass = request.POST.get('repeat_pass')
            if new_pass == repeat_pass:
                get_current = request.POST.get('current_pass')
                checker = check_password(get_current , request.user.password)
                if checker == True:
                    get_user = CustomUser.objects.get(id = request.user.id)
                    get_user.password = make_password(new_pass)
                    get_user.save()
                    messages.success(request , 'پسورد شما با موفقیت آپدیت شد')
                    return redirect('login1')
                else:
                    messages.warning(request , 'پسوردی که وارد کردید با پسورد فعلی شما متفاوت است')
            else:
                messages.warning(request , 'پسورد جدید شما با تکرار آن همخوانی ندارد')
        else:
            messages.warning(request ,'طول پسورد شما کمتر از 8 کاراکتر است')
    return render (request ,'profile/change_password.html')

@login_required
def change_details_page(request):
    if request.method == "POST":
        get_user = CustomUser.objects.get(id=request.user.id)
        flag= False

        if request.POST['username'] != '':
            try:
                check_user = CustomUser.objects.get(username=request.POST['username'])
            except:
                check_user = None
            if check_user == None:
                get_user.username = request.POST['username']
                flag= True
            else:
                messages.warning(request, 'یوزرنیم انتخابی شما وجود دارد')
                return render (request , 'profile/change_profile.html')
        if request.POST['first_name'] != '':
            get_user.first_name = request.POST['first_name']
            flag=True
        if request.POST['last_name'] != '':
            get_user.last_name = request.POST['last_name']
            flag=True
        if request.POST['email_address'] != '':
            if '@' in request.POST['email_address']:
                get_user.email = request.POST['email_address']
                flag = True
            else:
                messages.warning(request , 'ایمیل شما فرمت درستی ندارد')
                return render (request , 'profile/change_profile.html')
        if request.POST['phone_number'] !='':
            if request.POST['phone_number'][0] =='0':
                if len(request.POST['phone_number']) == 11:
                    get_user.phone_number = request.POST['phone_number']
                    flag=True
                else:
                    messages.warning(request , 'طول شماره ی شما باید 11 کاراکتر باشد')
                    return render (request , 'profile/change_profile.html')
            else:
                messages.warning(request , 'شماره ی شما باید با صفر شروع شود')
                return render (request , 'profile/change_profile.html')

        if flag== True:
            messages.success(request , 'پروفایل با موفقیت آپدیت شد')
            get_user.save()
        
            
    return render (request , 'profile/change_profile.html')