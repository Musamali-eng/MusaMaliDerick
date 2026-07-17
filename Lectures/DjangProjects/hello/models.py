from django.db import models

class Contact(models.Model):
    # Personal Information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    
    # Project Details
    subject = models.CharField(max_length=100)
    service_interest = models.CharField(max_length=50, blank=True, null=True)
    budget = models.CharField(max_length=50, blank=True, null=True)
    timeline = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    
    # Referral
    referral = models.CharField(max_length=50, blank=True, null=True)
    
    # Preferences
    newsletter = models.BooleanField(default=False)
    consent_marketing = models.BooleanField(default=False)
    consent = models.BooleanField(default=True)
    
    # File Attachment (store file path or just filename)
    attachment_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject} - {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Contacts"