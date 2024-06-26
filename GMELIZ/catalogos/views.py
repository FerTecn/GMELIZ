from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage #Para archivos y directorios
from django.contrib.auth.decorators import login_required #Forzar inicio de sesión

import os
from .models import Carrito, Categoria, DetallePedido, ItemCarrito, Pedido, Producto
from django.db.models import F, Sum
from .forms import CategoriaForm, ProductoForm
from django.db import transaction
from django.contrib.auth.decorators import user_passes_test



# Create your views here.
#CRUD Categoria Producto
@login_required(login_url='signin')
def accesodenegado(request):
    return render(request, 'denegado.html')

@login_required(login_url='signin')
def categoriaList(request):
    categorias = Categoria.objects.all()
    data = {'categorias' : categorias}
    return render(request, "categoriaList.html", data)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.has_perm('catalogos.add_categoria'), login_url='accesodenegado')
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
@user_passes_test(lambda u: u.has_perm('catalogos.change_categoria'), login_url='accesodenegado')
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
@user_passes_test(lambda u: u.has_perm('catalogos.delete_categoria'), login_url='accesodenegado')
def categoriaDelete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoriaList')
    return render(request, 'categoriaDelete.html', {'categoria': categoria})

# CRUD Productos
@login_required(login_url='signin')
def productoList(request):
    # Obtener todos los productos
    productos = Producto.objects.all()

    # Obtener categorías únicas
    categorias = Categoria.objects.all()

    # Filtrar por categoría si se ha seleccionado alguna
    categoria_seleccionada = request.GET.get('categoria')
    if categoria_seleccionada:
        productos = productos.filter(categoria=categoria_seleccionada)

    data = {
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, "productoList.html", data)

@login_required(login_url='signin')
def productoDetail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "productoDetails.html", {'producto': producto})

@login_required(login_url='signin')
@user_passes_test(lambda u: u.has_perm('catalogos.create_producto'), login_url='accesodenegado')
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
@user_passes_test(lambda u: u.has_perm('catalogos.change_producto'), login_url='accesodenegado')
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
@user_passes_test(lambda u: u.has_perm('catalogos.delete_producto'), login_url='accesodenegado')
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


def agregar_producto_carrito(request, producto_id):
    # Obtener el producto y la cantidad disponible en el inventario
    producto = get_object_or_404(Producto, pk=producto_id)
    cantidad_disponible = producto.inventario

    # Obtener el carrito del usuario
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    # Verificar si hay suficiente inventario para agregar el producto al carrito
    # # if carrito.productos.filter(pk=producto_id).count() < cantidad_disponible:
    if cantidad_disponible > 0:
        # Verificar si el producto ya está en el carrito
        if carrito.productos.filter(pk=producto_id).exists():
            # Si el producto ya está en el carrito, aumentar la cantidad en 1
            item_carrito = ItemCarrito.objects.get(carrito=carrito, producto=producto)
            item_carrito.cantidad += 1
            item_carrito.save()
        else:
            # Si el producto no está en el carrito, agregarlo con una cantidad de 1
            item_carrito = ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=1)
    else:
        # Si no hay suficiente inventario, mostrar un mensaje indicando que el producto no está disponible
        return render(request, 'producto_agotado.html', {'producto': producto})
        
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'carrito.html', {'carrito': carrito})

@transaction.atomic
def realizar_pedido(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    # Crear el pedido solo si el carrito no está vacío
    if carrito.productos.exists():
        pedido = Pedido.objects.create(usuario=request.user)

        # Crear detalles del pedido y asociar los productos al pedido con su respectiva cantidad
        for item_carrito in carrito.itemcarrito_set.all():
            DetallePedido.objects.create(pedido=pedido, producto=item_carrito.producto, cantidad=item_carrito.cantidad)

            # Reducir la cantidad disponible en el inventario para cada producto en el pedido
            item_carrito.producto.inventario -= item_carrito.cantidad
            item_carrito.producto.save()

        # Limpiar el carrito después de agregar los productos al pedido
        carrito.productos.clear()

        return redirect('detalle_pedido', pedido_id=pedido.id)
    else:
        # Si el carrito está vacío, redirigir al usuario a la página del carrito
        return redirect('ver_carrito')

def confirmar_pedido(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    total_productos = carrito.itemcarrito_set.all().count()
    total_pagar = carrito.total()

    if request.method == 'POST':
        pedido = Pedido.objects.create(usuario=request.user)
        pedido.productos.set(carrito.productos.all())
        carrito.productos.clear()
        return redirect('detalle_pedido', pedido_id=pedido.id)

    return render(request, 'confirmar_pedido.html', {'total_productos': total_productos, 'total_pagar': total_pagar})

def ver_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'pedidos.html', {'pedidos': pedidos})

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    detalles_pedido = DetallePedido.objects.filter(pedido=pedido)

    total_pagado = detalles_pedido.aggregate(total=Sum(F('producto__precio') * F('cantidad')))['total']

    return render(request, 'detalle_pedido.html', {'pedido': pedido, 'detalles_pedido': detalles_pedido, 'total_pagado': total_pagado})

def producto_agotado(request):
    # Aquí puedes agregar lógica adicional si es necesario
    return render(request, 'producto_agotado.html')

def eliminar_producto_carrito(request, producto_id):
    # Obtener el producto del carrito
    producto = get_object_or_404(ItemCarrito, pk=producto_id)
    # Eliminar el producto del carrito
    producto.delete()
    return redirect('ver_carrito')

def limpiar_carrito(request):
    # Obtener el carrito del usuario
    carrito = Carrito.objects.get(usuario=request.user)
    # Eliminar todos los productos del carrito
    carrito.productos.clear()
    return redirect('ver_carrito')

@login_required(login_url='signin')
def incrementar_cantidad(request, item_id):
    item_carrito = get_object_or_404(ItemCarrito, id=item_id)
    item_carrito.incrementar_cantidad()
    return redirect('ver_carrito')

@login_required(login_url='signin')
def decrementar_cantidad(request, item_id):
    item_carrito = get_object_or_404(ItemCarrito, id=item_id)
    item_carrito.decrementar_cantidad()
    return redirect('ver_carrito')