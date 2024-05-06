from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.http import JsonResponse #Devolver arreglos de datos RFID
from django.utils import formats #Dar formatos a las fechas
from django.core.files.storage import FileSystemStorage #Para archivos y directorios
from django.contrib.auth.decorators import login_required #Forzar inicio de sesión

import os
from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm

# Create your views here.
#CRUD Categoria Producto
@login_required(login_url='signin')
def categoriaList(request):
    categorias = Categoria.objects.all()
    data = {'categorias' : categorias}
    return render(request, "categoriaList.html", data)

@login_required(login_url='signin')
def categoriaCreate(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoriaList')
    else:
        form = CategoriaForm()
        return render(request, 'categoriaCreate.html', {'form' : form})

@login_required(login_url='signin')
def categoriaUpdate(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoriaList')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoriaUpdate.html', {'form': form})

@login_required(login_url='signin')
def categoriaDelete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoriaList')
    return render(request, 'categoriaDelete.html', {'categoria': categoria})

# CRUD Productos
@login_required(login_url='signin')
def productoList(request):
    productos = Producto.objects.all()
    data = {'productos' : productos}
    return render(request, "productoList.html", data)

@login_required(login_url='signin')
def productoCreate(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']

           # Verify if the code already exists
            if Producto.objects.filter(codigo=codigo).exists():
                error = 'Ya existe un producto con este Codigo.'
                return render(request, 'productoCreate.html', {'form': form, 'error': error})

            
            form.save()
            return redirect('productoList')
        # Return a response even if the form is not valid
        else:
            return render(request, 'productoCreate.html', {'form': form})
    else:
        form = ProductoForm()
        return render(request, 'productoCreate.html', {'form' : form})

@login_required(login_url='signin')
def productoUpdate(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            # Procesar la imagen
            imagen = request.FILES['imagen'] if 'imagen' in request.FILES else None

            # Si el producto no tiene imagen
            if not producto.imagen:
                # Sobrescribir la imagen existente
                producto.imagen = imagen
            else:
                imagenActual = producto.imagen
                if imagen:
                    # Eliminar la imagen existente
                    fs = FileSystemStorage()
                    fs.delete(producto.imagen.name)
                    # Sobrescribir la imagen existente
                    producto.imagen = imagen
                else:
                    producto.imagen = imagenActual

            form.save()
            return redirect('productoList')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productoUpdate.html', {'producto': producto,'form': form})

@login_required(login_url='signin')
def productoDelete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        # Eliminar la imagen
        if producto.imagen:
            fs = FileSystemStorage()
            fs.delete(producto.imagen.name)
        producto.delete()
        return redirect('productoList')
    return render(request, 'productoDelete.html', {'categoria': producto})

