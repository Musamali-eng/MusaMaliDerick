from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import ContactForm, SUBJECT_CHOICES, SERVICE_CHOICES, BUDGET_CHOICES, REFERRAL_CHOICES

def home(request):
    return render(request, 'home.html', {'page': 'home'})

def about(request):
    return render(request, 'about.html', {'page': 'about'})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data
            data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data.get('phone', 'Not provided'),
                'company': form.cleaned_data.get('company', 'Not provided'),
                'job_title': form.cleaned_data.get('job_title', 'Not provided'),
                'subject': dict(SUBJECT_CHOICES).get(form.cleaned_data['subject'], form.cleaned_data['subject']),
                'service': dict(SERVICE_CHOICES).get(form.cleaned_data.get('service_interest', ''), 'Not specified'),
                'budget': dict(BUDGET_CHOICES).get(form.cleaned_data.get('budget', ''), 'Not specified'),
                'timeline': form.cleaned_data.get('timeline', 'Not specified'),
                'message': form.cleaned_data['message'],
                'referral': dict(REFERRAL_CHOICES).get(form.cleaned_data.get('referral', ''), 'Not specified'),
                'newsletter': form.cleaned_data.get('newsletter', False),
                'consent_marketing': form.cleaned_data.get('consent_marketing', False),
                'page': 'success',  # For navigation highlighting
            }
            
            # Handle file attachment
            attachment = form.cleaned_data.get('attachment')
            attachment_info = "No attachment"
            if attachment:
                attachment_info = f"Filename: {attachment.name}\nSize: {attachment.size} bytes\nType: {attachment.content_type}"
            
            # Build professional email
            email_message = f"""
            ╔═══════════════════════════════════════════════════════════╗
            ║          🆕 NEW CONTACT FORM SUBMISSION                  ║
            ╚═══════════════════════════════════════════════════════════╝

            📋 PERSONAL INFORMATION
            ───────────────────────────────────────────────
            Full Name:     {data['name']}
            Email:         {data['email']}
            Phone:         {data['phone']}
            Company:       {data['company']}
            Job Title:     {data['job_title']}

            📌 PROJECT DETAILS
            ───────────────────────────────────────────────
            Subject:       {data['subject']}
            Service:       {data['service']}
            Budget:        {data['budget']}
            Timeline:      {data['timeline']}

            📝 MESSAGE
            ───────────────────────────────────────────────
            {data['message']}

            🔗 REFERRAL
            ───────────────────────────────────────────────
            How found us:  {data['referral']}

            📎 ATTACHMENT
            ───────────────────────────────────────────────
            {attachment_info}

            📧 PREFERENCES
            ───────────────────────────────────────────────
            Newsletter:    {'✅ Yes' if data['newsletter'] else '❌ No'}
            Marketing:     {'✅ Yes' if data['consent_marketing'] else '❌ No'}

            📅 SUBMITTED
            ───────────────────────────────────────────────
            Date/Time:     {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}
            IP Address:    [User IP would be logged here]

            ═══════════════════════════════════════════════════════════
            This message was sent from the MyDjango website contact form.
            """
            
            # Send email
            try:
                send_mail(
                    subject=f"New Contact: {data['subject']}",
                    message=email_message,
                    from_email=data['email'],
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                print("✅ Email sent successfully!")
            except Exception as e:
                print(f"❌ Email failed: {e}")
            
            return render(request, 'success.html', data)
        else:
            # Form has errors
            return render(request, 'contact.html', {
                'form': form,
                'page': 'contact'
            })
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {
        'form': form,
        'page': 'contact'
    })