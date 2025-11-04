from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at', 'interview_scheduled_at']
    list_filter = ['status', 'applied_at', 'reviewed_at']
    search_fields = ['applicant__email', 'applicant__name', 'job__title', 'job__company_name']
    readonly_fields = ['id', 'applied_at', 'updated_at']
    
    fieldsets = (
        ('Application Info', {
            'fields': ('job', 'applicant', 'cover_letter', 'resume', 'portfolio_url')
        }),
        ('Status', {
            'fields': ('status', 'status_notes', 'reviewed_at')
        }),
        ('Interview', {
            'fields': ('interview_scheduled_at', 'interview_location', 'interview_notes')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at')
        }),
    )
