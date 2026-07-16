from django.shortcuts import render
from .forms import ContactForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # You can save to database or send email here
            
            # Redirect to success page with name
            return render(request, 'success.html', {'name': name})
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})