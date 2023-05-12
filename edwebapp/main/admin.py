from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
#     list_filter = ('is_active',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_admin', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email', 'username')
#     ordering = ('email',)
#     filter_horizontal = ()


admin.site.register(User)
admin.site.register(Course)
