from django.shortcuts import render ,redirect
from core.forms import SignupForm,LoginForm
from item.models import Item,Category
from django.contrib.auth import  login
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