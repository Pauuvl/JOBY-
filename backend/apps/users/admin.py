from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model"""
    
    list_display = ['email', 'name', 'username', 'is_active', 'email_verified', 'created_at']
    list_filter = ['is_active', 'email_verified', 'created_at']
    search_fields = ['email', 'name', 'username']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'location', 'profile_image', 'resume')}),
        ('Professional Info', {'fields': ('experience', 'education', 'skills')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'email_verified')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
