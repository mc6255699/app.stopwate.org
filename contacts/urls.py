from django.urls import path
from . import views
from .views import *

app_name = 'contacts'

urlpatterns = [
    #path('', views.index, name='contact_home'),
    path('', ContactListView.as_view(), name='list'),  # list all contacts
    path('add/', ContactCreateView.as_view(), name='add'),  # the create form
    path("<int:pk>/", ContactDetailView.as_view(), name="detail"),  # 
    path("<int:pk>/edit/", ContactUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ContactDeleteView.as_view(), name="delete"),

]

