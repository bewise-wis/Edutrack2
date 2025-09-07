from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # This should come first for login
    path('dashboard/', include('dashboard.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('classes/', include('classes.urls')),
    path('subjects/', include('subjects.urls')),
    path('results/', include('results.urls')),
    path('reports/', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)