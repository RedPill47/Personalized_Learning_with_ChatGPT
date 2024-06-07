from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

]

urlpatterns += static('/output_files/', document_root=os.path.join(settings.BASE_DIR, 'output_files'))
