from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['subject', 'newsletter', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'company', 'job_title')
        }),
        ('Project Details', {
            'fields': ('subject', 'service_interest', 'budget', 'timeline', 'message')
        }),
        ('Referral & Preferences', {
            'fields': ('referral', 'newsletter', 'consent_marketing', 'consent')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )