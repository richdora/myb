from django.contrib import admin
from .models import Movie, Tag

class MovieAdmin(admin.ModelAdmin):
    list_display = ('owner', 'youtube_link')
    search_fields = ('owner', 'owner__username')
    list_filter = ('owner', 'tags',)

    def display_thumbnail_url(self, obj):
        return obj.thumbnail_url
    display_thumbnail_url.short_description = 'Thumbnail URL'

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Movie, MovieAdmin)
admin.site.register(Tag, TagAdmin)
