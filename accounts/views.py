from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User , auth
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user= auth.authenticate(username=username,password=password)
        #user= User.objects.filter(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'authentication failed!...')
            return redirect('login')

    else:
        return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'E-mail already taken.')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username taken.')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                print('user created')
                mydict={'firstname':first_name}
                html_template = 'register_email.html'
                html_message = render_to_string(html_template, context=mydict)
                subject = 'Welcome to TODO list Verse'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                message = EmailMessage(subject, html_message,
                                        email_from, recipient_list)
                message.content_subtype = 'html'
                message.send()
                return redirect('login')
        else:
            messages.info(request,'password1 and password2 didn\'t match.')
        return redirect('register')
    
    else:
        return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

