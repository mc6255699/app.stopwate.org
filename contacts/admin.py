
# Register your models here.

from django.contrib import admin
from .models import Organization, Contact, ContactList

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'zip_code')
    search_fields = ('name', 'city', 'state', 'zip_code')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job_title', 'email', 'phone_number', 'organization')
    search_fields = ('first_name', 'last_name', 'email', 'job_title')
    list_filter = ('organization',)

@admin.register(ContactList)
class ContactListAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    search_fields = ('name', 'description')
    filter_horizontal = ('contacts', 'sublists')  # Better widget for many-to-many

