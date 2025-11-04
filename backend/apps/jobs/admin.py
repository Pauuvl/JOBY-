from django.contrib import admin
from .models import Job, SavedJob


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'location', 'job_type', 'posted_at', 'is_active', 'views_count']
    list_filter = ['job_type', 'experience_level', 'remote_ok', 'is_active', 'posted_at']
    search_fields = ['title', 'company_name', 'location', 'description']
    prepopulated_fields = {'slug': ('title', 'company_name')}
    readonly_fields = ['id', 'posted_at', 'updated_at', 'views_count', 'slug']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company_name', 'company_logo', 'location', 'remote_ok')
        }),
        ('Job Details', {
            'fields': ('job_type', 'experience_level', 'description', 'requirements', 
                      'responsibilities', 'benefits', 'skills_required')
        }),
        ('Salary Information', {
            'fields': ('salary_min', 'salary_max', 'salary_currency')
        }),
        ('Application', {
            'fields': ('application_url', 'application_email')
        }),
        ('Metadata', {
            'fields': ('posted_by', 'posted_at', 'updated_at', 'expires_at', 
                      'is_active', 'views_count', 'slug')
        }),
    )


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__email', 'user__name', 'job__title']
    readonly_fields = ['id', 'saved_at']
