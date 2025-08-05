from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from core.views import full_logout


app_name = "core"
urlpatterns = [
    path('user/debug/', views.user_debug, name='user_debug'),
    path('', views.home, name='home'),
    path('hub/', views.hub, name='hub'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', full_logout, name="full_logout"),
]


# Serve uploaded files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
