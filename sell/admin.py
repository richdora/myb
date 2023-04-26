from django.contrib import admin
from .models import SellItem

class SellItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
    list_filter = ('owner', 'created_date')
    search_fields = ('title', 'comment')
    readonly_fields = ('created_date',)

admin.site.register(SellItem, SellItemAdmin)
