from django.urls import  path
from . import views

from .forms import LoginForm

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    # path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view , name='login'),
]