from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    # ---------------------------
    # Contact Records
    # ---------------------------
    path('', views.ContactListView.as_view(), name='list'),             # List all contacts
    path('add/', views.ContactCreateView.as_view(), name='add'),                        # Simple Contact Add FOrm 
    path('<int:pk>/', views.contact_detail, name='detail'),             # Unified detail view
    path('<int:pk>/edit/', views.contact_edit, name='update'),          # Unified edit form
    path('<int:pk>/delete/', views.ContactDeleteView.as_view(), name='delete'),

    # ---------------------------
    # Contact list membership AJAX
    # ---------------------------
    path('<int:pk>/lists/add/', views.add_contact_to_list, name='contact_list_add'),
    path('<int:pk>/lists/remove/', views.remove_contact_from_list, name='contact_list_remove'),
    path('search_ajax/', views.contact_search_ajax, name='contact_search_ajax'),
    path('contactlist_add_contact/<int:list_id>/<int:contact_id>/', 
         views.contactlist_add_contact, name='contactlist_add_contact'),

    # ---------------------------
    # Contact Lists (Lists of Contacts)
    # ---------------------------
    path('lists/', views.ContactListListView.as_view(), name='contactlist_list'),           # List all contact lists
    path('lists/new/', views.ContactListCreateView.as_view(), name='contactlist_create'),   # Create new contact list
    path('lists/<int:pk>/edit/', views.ContactListUpdateView.as_view(), name='contactlist_edit'),  # Edit list
    path('lists/search/', views.search_contact_lists, name='list_search'),                  # AJAX search
    path('lists/<int:pk>/remove/<int:contact_id>/', views.contactlist_remove_contact, name='contactlist_remove_contact'),
    path('lists/<int:list_id>/add_sublist/', views.add_sublist_to_list, name='add_sublist_to_list'),
    path('lists/<int:list_id>/remove_sublist/', views.remove_sublist_from_list, name='remove_sublist_from_list'),

    # ---------------------------
    # API endpoint
    # ---------------------------
    path('<int:pk>/api/', views.contact_detail_api, name='contact_detail_api'),
]
