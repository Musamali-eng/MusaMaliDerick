from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import ContactForm, SUBJECT_CHOICES, SERVICE_CHOICES, BUDGET_CHOICES, REFERRAL_CHOICES
from .models import Contact  # ← Add this import

def home(request):
    return render(request, 'home.html', {'page': 'home'})

def about(request):
    return render(request, 'about.html', {'page': 'about'})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', '')
            company = form.cleaned_data.get('company', '')
            job_title = form.cleaned_data.get('job_title', '')
            subject = dict(SUBJECT_CHOICES).get(form.cleaned_data['subject'], form.cleaned_data['subject'])
            service_interest = dict(SERVICE_CHOICES).get(form.cleaned_data.get('service_interest', ''), '')
            budget = dict(BUDGET_CHOICES).get(form.cleaned_data.get('budget', ''), '')
            timeline = form.cleaned_data.get('timeline', '')
            message = form.cleaned_data['message']
            referral = dict(REFERRAL_CHOICES).get(form.cleaned_data.get('referral', ''), '')
            newsletter = form.cleaned_data.get('newsletter', False)
            consent_marketing = form.cleaned_data.get('consent_marketing', False)
            consent = form.cleaned_data.get('consent', True)
            
            # Handle file attachment
            attachment = form.cleaned_data.get('attachment')
            attachment_name = attachment.name if attachment else ''
            
            # ===== SAVE TO DATABASE =====
            contact = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                company=company,
                job_title=job_title,
                subject=subject,
                service_interest=service_interest,
                budget=budget,
                timeline=timeline,
                message=message,
                referral=referral,
                newsletter=newsletter,
                consent_marketing=consent_marketing,
                consent=consent,
                attachment_name=attachment_name,
            )
            print(f"✅ Contact saved to database! ID: {contact.id}")
            
            # Handle file save if needed
            if attachment:
                # You can save the file to media folder
                import os
                from django.core.files.storage import default_storage
                file_path = f'contact_attachments/{contact.id}_{attachment.name}'
                saved_path = default_storage.save(file_path, attachment)
                print(f"📎 File saved: {saved_path}")
            
            # ===== SEND EMAIL =====
            attachment_info = f"Filename: {attachment_name}" if attachment_name else "No attachment"
            
            email_message = f"""
            ╔═══════════════════════════════════════════════════════════╗
            ║          🆕 NEW CONTACT FORM SUBMISSION                  ║
            ╚═══════════════════════════════════════════════════════════╝

            📋 PERSONAL INFORMATION
            ───────────────────────────────────────────────
            Name:          {name}
            Email:         {email}
            Phone:         {phone or 'Not provided'}
            Company:       {company or 'Not provided'}
            Job Title:     {job_title or 'Not provided'}

            📌 PROJECT DETAILS
            ───────────────────────────────────────────────
            Subject:       {subject}
            Service:       {service_interest or 'Not specified'}
            Budget:        {budget or 'Not specified'}
            Timeline:      {timeline or 'Not specified'}

            📝 MESSAGE
            ───────────────────────────────────────────────
            {message}

            🔗 REFERRAL
            ───────────────────────────────────────────────
            How found us:  {referral or 'Not specified'}

            📎 ATTACHMENT
            ───────────────────────────────────────────────
            {attachment_info}

            📧 PREFERENCES
            ───────────────────────────────────────────────
            Newsletter:    {'✅ Yes' if newsletter else '❌ No'}
            Marketing:     {'✅ Yes' if consent_marketing else '❌ No'}

            📅 SUBMITTED
            ───────────────────────────────────────────────
            Date/Time:     {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}
            Contact ID:    {contact.id}

            ═══════════════════════════════════════════════════════════
            This message was sent from the MyDjango website contact form.
            """
            
            # Send email
            try:
                send_mail(
                    subject=f"New Contact: {subject} - {name}",
                    message=email_message,
                    from_email=email,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                print("✅ Email sent successfully!")
            except Exception as e:
                print(f"❌ Email failed: {e}")
            
            # Prepare data for success page
            data = {
                'name': name,
                'email': email,
                'phone': phone or 'Not provided',
                'company': company or 'Not provided',
                'job_title': job_title or 'Not provided',
                'subject': subject,
                'service': service_interest or 'Not specified',
                'budget': budget or 'Not specified',
                'timeline': timeline or 'Not specified',
                'referral': referral or 'Not specified',
                'newsletter': newsletter,
                'consent_marketing': consent_marketing,
                'page': 'success',
            }
            
            return render(request, 'success.html', data)
        else:
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