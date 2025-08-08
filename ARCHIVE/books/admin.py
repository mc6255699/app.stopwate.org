from django.contrib import admin
from .models import Book, Genre

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_date", "genre"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]           # ✅ Was: "name", now: ["name"]
    search_fields = ["name"]          # ✅ Was: "name", now: ["name"]
