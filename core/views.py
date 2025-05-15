from django.shortcuts import render ,redirect
from core.forms import SignupForm,LoginForm
from item.models import Item,Category
from django.contrib.auth import  login
from django.conf import settings
import random
from django.core.mail import send_mail

def index(request):
    items=Item.objects.filter(is_sold=False)[:6]
    categories=Category.objects.all()
    return render(request,'core/index.html',{
        'items':items,
        'categories':categories
    })

def contact(request):
    return render(request,'core/contact.html')

'''
def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html',{
        'form':form
    })
'''
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # print(request.POST)  # Debug: see submitted data
        # print(form.errors)   # Debug: see validation errors
        if form.is_valid():
            form.save()
            return redirect('/login/')  # Use named URL pattern
        # If form is invalid, it will fall through to render with errors
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        print("POST data:", request.POST)  # Debug
        print("Form errors:", form.errors)  # Debug
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')  # Redirect to homepage
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {
        'form': form
    })

# def generate_numeric_otp():
#     return str(random.randint(1000, 9999))

# # Send email
# def send_email(otp, recipient_list):
#     subject = 'OTP for 2FA Login'
#     message = f'Your OTP for 2FA Authentication: {otp}'
#     from_email = settings.EMAIL_HOST_USER
#     try:
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     except Exception as e:
#         raise Exception(f"Failed to send email: {str(e)}")
    

    