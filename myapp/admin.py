from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import PrivateMessage

class CustomUserAdmin(UserAdmin):
    # You can customize the fields you want to display in the admin site
    # by modifying the list_display attribute
    list_display = ('username', 'is_staff', 'is_active', 'is_superuser')

    # You can also customize the fields to be used in the add user form
    # by modifying the add_fieldsets attribute


class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'timestamp', 'read')
    list_filter = ('sender', 'recipient', 'read')
    search_fields = ('sender__username', 'recipient__username', 'content')

admin.site.register(PrivateMessage, PrivateMessageAdmin)


admin.site.register(CustomUser, CustomUserAdmin)
