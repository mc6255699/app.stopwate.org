# cc_bot/admin.py
from django.contrib import admin
from .models import CCName, CCRequest

admin.site.register(CCName)
admin.site.register(CCRequest)