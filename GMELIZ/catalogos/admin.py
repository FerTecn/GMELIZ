from django.contrib import admin

# Register your models here.
from catalogos.models import Categoria, Producto, Carrito, Pedido
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(Pedido)

