
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect


def login_placeholder(request):
    return HttpResponseRedirect("/")  # fallback to home


urlpatterns = [



    path('', include('core.urls')),  # and hub will be at /
    path('auth/', include("django_auth_adfs.urls")),
    path('core/', include("core.urls", namespace="core")),
    path('admin/', admin.site.urls),
    path('invoices/', include('invoices.urls')),
    path('ccbot/', include('ccbot.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
