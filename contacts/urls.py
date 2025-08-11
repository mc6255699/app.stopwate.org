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


    path('lists/search/', views.search_contact_lists, name='list_search'),
    path('<int:pk>/lists/add/', views.add_contact_to_list, name='contact_list_add'),
    path('<int:pk>/lists/remove/', views.remove_contact_from_list, name='contact_list_remove'),

]


