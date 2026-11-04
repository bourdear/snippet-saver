from django.contrib import admin

from .models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'created_at']
    list_filter = ['language']
    search_fields = ['title', 'code']
