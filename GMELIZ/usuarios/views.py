from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import SignupForm, SigninForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email']
                    )
                    user.save()

                    # Asignar grupo basado en la elección del usuario
                    user_type = form.cleaned_data['user_type']
                    group = Group.objects.get(name=user_type)
                    user.groups.add(group)

                    login(request, user)
                    return redirect('inicio')
                except IntegrityError:
                    return render(request, 'signup.html', {'form': form, 'error': 'Nombre de usuario ya existe, elija otro.'})
            else:
                return render(request, 'signup.html', {'form': form, 'error': 'Contraseñas no coinciden.'})
        else:
            return render(request, 'signup.html', {'form': form, 'error': 'Formulario no válido.'})
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

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