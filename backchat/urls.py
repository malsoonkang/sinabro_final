from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from accounts import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include('accounts.urls')),
    path('board/', include('board.urls')),
    path("", include('board.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)