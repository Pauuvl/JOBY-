from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, MotivationalMessage


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


@admin.register(MotivationalMessage)
class MotivationalMessageAdmin(admin.ModelAdmin):
    """Admin configuration for MotivationalMessage model"""
    
    list_display = ['message_preview', 'author', 'category', 'priority', 'times_shown', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['message', 'author']
    ordering = ['-priority', '-created_at']
    list_editable = ['is_active', 'priority']
    
    fieldsets = (
        (None, {'fields': ('message', 'author', 'category')}),
        ('Configuración', {'fields': ('is_active', 'priority')}),
        ('Estadísticas', {'fields': ('times_shown',)}),
        ('Fechas', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['times_shown', 'created_at', 'updated_at']
    
    def message_preview(self, obj):
        """Show a preview of the message"""
        return obj.message[:80] + '...' if len(obj.message) > 80 else obj.message
    message_preview.short_description = 'Mensaje'
    
    actions = ['activate_messages', 'deactivate_messages', 'reset_shown_count']
    
    def activate_messages(self, request, queryset):
        """Activate selected messages"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} mensajes activados.')
    activate_messages.short_description = 'Activar mensajes seleccionados'
    
    def deactivate_messages(self, request, queryset):
        """Deactivate selected messages"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} mensajes desactivados.')
    deactivate_messages.short_description = 'Desactivar mensajes seleccionados'
    
    def reset_shown_count(self, request, queryset):
        """Reset shown count to zero"""
        updated = queryset.update(times_shown=0)
        self.message_user(request, f'Contador reiniciado para {updated} mensajes.')
    reset_shown_count.short_description = 'Reiniciar contador de veces mostrado'
