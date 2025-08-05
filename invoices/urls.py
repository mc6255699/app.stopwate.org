# invoices/urls.py
from django.urls import path
from . import views

app_name = 'invoices'  # This allows us to use namespaced URLs for the invoices app

urlpatterns = [
    path('upload/', views.upload_invoice, name='upload_invoice'),
#    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('search/', views.search_invoice, name='search_invoice'),
]
