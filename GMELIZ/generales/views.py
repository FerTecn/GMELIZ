from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='signin')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='signin')
def about(request):
    return render(request, 'about.html')

@login_required(login_url='signin')
def contactus(request):
    return render(request, 'contactus.html')