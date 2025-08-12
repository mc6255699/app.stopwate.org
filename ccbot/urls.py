from django.urls import path
from . import views

app_name = "ccbot"

urlpatterns = [
    path('', views.request_card, name='request_card'),
    path('cc_log/', views.cc_log, name='cc_log'),
    path("cc_log/export/", views.cc_requests_export_csv, name="cc_requests_export_csv"),
]