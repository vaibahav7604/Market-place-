from django.urls import path
from . import views

app_name = 'item'
urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('', views.non, name='non'),
    path('item/<int:pk>/conversation/new/', views.new_conversation, name='conversation_new'),
    path('conversation/<int:pk>/', views.conversation_chat, name='conversation'),
    path('inbox/', views.inbox, name='inbox'),
]