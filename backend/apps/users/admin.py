from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, MotivationalMessage, JobAlertPreference


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


@admin.register(JobAlertPreference)
class JobAlertPreferenceAdmin(admin.ModelAdmin):
    """Admin configuration for JobAlertPreference model"""
    
    list_display = ['user', 'is_enabled', 'frequency', 'match_by_skills', 'match_by_location', 'remote_only', 'last_alert_sent']
    list_filter = ['is_enabled', 'frequency', 'remote_only', 'match_by_skills', 'match_by_location']
    search_fields = ['user__email', 'user__name']
    ordering = ['-created_at']
    list_editable = ['is_enabled', 'frequency']
    
    fieldsets = (
        ('Usuario', {'fields': ('user',)}),
        ('Configuración General', {'fields': ('is_enabled', 'frequency')}),
        ('Criterios de Matching', {'fields': ('match_by_skills', 'match_by_location', 'match_by_experience')}),
        ('Preferencias de Trabajo', {'fields': ('preferred_job_types', 'preferred_locations', 'remote_only', 'min_salary')}),
        ('Información', {'fields': ('last_alert_sent', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ['last_alert_sent', 'created_at', 'updated_at']
    
    actions = ['enable_alerts', 'disable_alerts', 'send_test_alert']
    
    def enable_alerts(self, request, queryset):
        """Enable alerts for selected users"""
        updated = queryset.update(is_enabled=True)
        self.message_user(request, f'Alertas activadas para {updated} usuarios.')
    enable_alerts.short_description = 'Activar alertas'
    
    def disable_alerts(self, request, queryset):
        """Disable alerts for selected users"""
        updated = queryset.update(is_enabled=False)
        self.message_user(request, f'Alertas desactivadas para {updated} usuarios.')
    disable_alerts.short_description = 'Desactivar alertas'
    
    def send_test_alert(self, request, queryset):
        """Send test alert to selected users"""
        from apps.jobs.services import JobMatchingService
        sent = 0
        for preference in queryset:
            notification = JobMatchingService.check_new_jobs_for_user(preference.user)
            if notification:
                sent += 1
        self.message_user(request, f'Alertas enviadas a {sent} usuarios.')
    send_test_alert.short_description = 'Enviar alerta de prueba'
