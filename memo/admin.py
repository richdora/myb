from django.contrib import admin
from .models import Memo, Tag

class MemoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_at', 'updated_at',)
    search_fields = ('owner__username',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Memo, MemoAdmin)
admin.site.register(Tag, TagAdmin)
