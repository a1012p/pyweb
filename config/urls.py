from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from pybo.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',base_views.index,name='index'),
    path('pybo/',include('pybo.urls')),
    path('common/',include('common.urls')),
]
urlpatterns +=  static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
