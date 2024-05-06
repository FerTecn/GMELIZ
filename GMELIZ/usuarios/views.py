from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import SignupForm, SigninForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username = request.POST['username'], 
                    password = request.POST['password1'],
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email']
                    )
                user.save()
                login(request, user)
                return redirect('inicio')
            except:
                return render(request, 'signup.html', {'form': SignupForm, 'error': 'Nombre de usuario ya existe, elija otro.'})
        return render(request, 'signup.html', {'form': SignupForm, 'error': 'Contraseñas no coinciden.'})
    else:
        return render(request, 'signup.html', {'form': SignupForm})

def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': SigninForm})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': SigninForm, 'error': 'Usuario y/o contraseña incorrectos'})
        else:
            login(request, user)
            return redirect('inicio')
        