from django.urls import path
from . import views
from .views import *

app_name = 'contacts'

urlpatterns = [
    # Contact Records
    path('', ContactListView.as_view(), name='list'),  # list all contacts
    path('add/', ContactCreateView.as_view(), name='add'),  # the create form
    path("<int:pk>/", ContactDetailView.as_view(), name="detail"),  # 
    path("<int:pk>/edit/", ContactUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ContactDeleteView.as_view(), name="delete"),

    # Contact List Records 
    path("lists/", ContactListListView.as_view(), name="contactlist_list"),
    path("lists/new/", ContactListCreateView.as_view(), name="contactlist_create"),
    path("lists/<int:pk>/edit/", ContactListUpdateView.as_view(), name="contactlist_update"),

    # path('list_list', ContactListListView.as_view(), name='list_list'),  # list all contact lists
    # path('list_add/', ContactListCreateView.as_view(), name='list_add'),  # the create form
    # path("<int:pk>/list_edit/", ContactListUpdateView.as_view(), name="list_update"),
    # path("<int:pk>/list_create/", ContactListCreateView.as_view(), name="list_delete"),
]

