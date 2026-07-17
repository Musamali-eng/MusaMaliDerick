from django import forms
from django.core.validators import FileExtensionValidator
from django_recaptcha.fields import ReCaptchaField

# Subject Choices
SUBJECT_CHOICES = [
    ('', 'Select a subject...'),
    ('general', 'General Inquiry'),
    ('support', 'Technical Support'),
    ('sales', 'Sales / Pricing'),
    ('partnership', 'Partnership Opportunity'),
    ('feedback', 'Feedback'),
    ('careers', 'Careers / Jobs'),
    ('press', 'Press / Media'),
    ('events', 'Events / Speaking'),
    ('investment', 'Investment / Funding'),
]

# Service Interest Choices
SERVICE_CHOICES = [
    ('', 'Select a service...'),
    ('web', 'Web Development'),
    ('mobile', 'Mobile App Development'),
    ('design', 'UI/UX Design'),
    ('cloud', 'Cloud Solutions'),
    ('consulting', 'Technical Consulting'),
    ('training', 'Training & Workshops'),
    ('other', 'Other'),
]

# Budget Range Choices
BUDGET_CHOICES = [
    ('', 'Select budget range...'),
    ('under_5000', 'Under $5,000'),
    ('5000_10000', '$5,000 - $10,000'),
    ('10000_25000', '$10,000 - $25,000'),
    ('25000_50000', '$25,000 - $50,000'),
    ('50000_plus', '$50,000+'),
    ('not_sure', 'Not sure / Need quote'),
]

# How Did You Find Us
REFERRAL_CHOICES = [
    ('', 'How did you find us?'),
    ('google', 'Google Search'),
    ('social_media', 'Social Media'),
    ('referral', 'Friend / Colleague Referral'),
    ('blog', 'Blog / Article'),
    ('event', 'Conference / Event'),
    ('email', 'Email Newsletter'),
    ('other', 'Other'),
]


class ContactForm(forms.Form):
    # ===== PERSONAL INFORMATION =====
    name = forms.CharField(
        max_length=100,
        label='Full Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'class': 'form-control'
        })
    )

    phone = forms.CharField(
        max_length=20,
        label='Phone Number',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+1 (555) 123-4567',
            'class': 'form-control'
        })
    )

    company = forms.CharField(
        max_length=100,
        label='Company Name',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your company name',
            'class': 'form-control'
        })
    )

    job_title = forms.CharField(
        max_length=100,
        label='Job Title',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., CEO, Developer, Manager',
            'class': 'form-control'
        })
    )

    # ===== PROJECT INFORMATION =====
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        label='Subject',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    service_interest = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        label='Service Interest',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    budget = forms.ChoiceField(
        choices=BUDGET_CHOICES,
        label='Budget Range',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    timeline = forms.CharField(
        max_length=100,
        label='Project Timeline',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., 1 month, 3 months, ASAP',
            'class': 'form-control'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about your project, goals, and how we can help...',
            'rows': 6,
            'class': 'form-control'
        }),
        label='Message'
    )

    # ===== ATTACHMENTS =====
    attachment = forms.FileField(
        required=False,
        label='Attach File (Optional)',
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt', 'zip']
        )],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png,.txt,.zip'
        })
    )

    # ===== REFERRAL =====
    referral = forms.ChoiceField(
        choices=REFERRAL_CHOICES,
        label='How did you find us?',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    # ===== CONSENT & PREFERENCES =====
    consent = forms.BooleanField(
        required=True,
        label='I agree to the Privacy Policy and consent to my data being stored.',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox'
        })
    )

    consent_marketing = forms.BooleanField(
        required=False,
        label='I agree to receive marketing communications via email',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox'
        })
    )

    newsletter = forms.BooleanField(
        required=False,
        label='Subscribe to our monthly newsletter for updates and tips',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox'
        })
    )

    # ===== RECAPTCHA =====
    captcha = ReCaptchaField()

    # ===== VALIDATION =====
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) < 10:
            raise forms.ValidationError("Please enter a valid phone number with at least 10 digits.")
        return phone

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 20:
            raise forms.ValidationError("Message must be at least 20 characters long.")
        return message