from django.contrib import admin
from .models import Photo, Tag

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'longitude', 'latitude', 'created_date')
    list_filter = ('user', 'tags')
    search_fields = ('comment', 'tags__name')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tag, TagAdmin)
