
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from core.views import index,contact
from django.conf.urls.static import static
urlpatterns = [
    path('',include('core.urls')),
    path('item/',include('item.urls')),
    path('',include('dashboard.urls')),

    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
