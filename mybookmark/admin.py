from django.contrib import admin
from .models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'youtube_link',)
    search_fields = ('youtube_link',)

admin.site.register(Bookmark, BookmarkAdmin)
