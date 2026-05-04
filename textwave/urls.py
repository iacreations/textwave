from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('contacts/', include('apps.contacts.urls')),
    path('campaigns/', include('apps.campaigns.urls')),
    path('reports/', include('apps.reports.urls')),
    path('billing/', include('apps.billing.urls')),
    path('', include('apps.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
