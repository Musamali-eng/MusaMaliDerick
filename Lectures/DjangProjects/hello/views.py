from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, World! Welcome to Django!")

def about(request):
    return HttpResponse("This is the about page.")