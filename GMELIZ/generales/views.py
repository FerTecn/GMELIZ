from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required


from catalogos.models import Producto  # Importa el modelo Producto desde la aplicación catalogos

# Create your views here.
@login_required(login_url='signin')
def home(request):
    productos = Producto.objects.all()[:8]  # Obtén los primeros 8 productos
    return render(request, 'home.html', {'productos': productos})

@login_required(login_url='signin')
def about(request):
    return render(request, 'about.html')

@login_required(login_url='signin')
def contactus(request):
    return render(request, 'contactus.html')