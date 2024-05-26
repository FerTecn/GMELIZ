from django.db import models
from django.contrib.auth.models import User, Permission, Group

import os
# # Create your models here.

def imagen_producto_path(instance, filename):
    # Generar el nombre de archivo utilizando el codigo y la extensión original
    ext = filename.split('.')[-1]
    new_filename = f"{instance.codigo}.{ext}"
    # Devolver la ruta completa
    return os.path.join('GMELIZ/static/img/productos/', new_filename)


class Categoria(models.Model):
    categoria = models.CharField(max_length=50,null=False)

    def __str__(self):
        return self.categoria

class Producto(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    producto = models.CharField(max_length=50,null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(null=True)
    imagen = models.ImageField(upload_to=imagen_producto_path, null=True, blank=True)
    inventario = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s de tipo %s a costo de %s" % (self.categoria, self.producto, self.precio) 

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def total(self):
        return sum(item.subtotal() for item in self.itemcarrito_set.all())
    
    def totalproductos(self):
        return sum(item.productostotal() for item in self.itemcarrito_set.all())
    

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad
    
    def productostotal(self):
        return self.cantidad
    
    def incrementar_cantidad(self):
        if self.cantidad < self.producto.inventario:
            self.cantidad += 1
            self.save()
    
    def decrementar_cantidad(self):
        if self.cantidad > 1:
            self.cantidad -= 1
            self.save()
    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_realizado = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    ESTADOS = (
        ('Pendiente', 'Pendiente'),
        ('Completado', 'Completado'),
    )
    estatus = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    productos = models.ManyToManyField(Producto, through='DetallePedido')

    def __str__(self):
        return f"Pedido #{self.pk} de {self.usuario.username}"
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.producto} en Pedido #{self.pedido.pk}"