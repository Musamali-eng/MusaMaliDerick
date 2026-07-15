from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm

def home(request):
    return HttpResponse("Hello, World! Welcome to Django!")

def about(request):
    return HttpResponse("This is the about page.")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Process the data (send email, save to database, etc.)
            return HttpResponse(f"Thank you {name}! Your message has been sent.")
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})