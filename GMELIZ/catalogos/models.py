from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

import os

# Create your models here.
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

    def calcular_total(self):
        total = sum(item.subtotal() for item in self.itemcarrito_set.all())
        return total

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

class Pedido(models.Model):
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)