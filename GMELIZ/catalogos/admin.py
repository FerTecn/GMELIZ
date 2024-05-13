from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from .models import Categoria, Producto, Carrito, Pedido

# Registro de modelos
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(Pedido)

# Función para configurar grupos y permisos
def configurar_grupos_y_permisos():
    # Crear grupos
    group_vendedor, created = Group.objects.get_or_create(name='Vendedor')
    group_cliente, created = Group.objects.get_or_create(name='Cliente')

    

    # Obtener permisos específicos necesarios para vistas de categoría y producto
    permisos_categoria = Permission.objects.filter(codename__in=['add_categoria', 'change_categoria', 'delete_categoria'])
    permisos_producto = Permission.objects.filter(codename__in=['add_producto', 'change_producto', 'delete_producto'])
    permisos_item_carrito =  Permission.objects.filter(codename__in=['view_itemcarrito', 'add_itemcarrito', 'change_itemcarrito', 'deleteitem_carrito'])
    permisos_carrito =  Permission.objects.filter(codename__in=['view_carrito', 'add_carrito', 'change_carrito', 'delete_carrito'])
    permisos_carrito =  Permission.objects.filter(codename__in=['view_carrito', 'add_carrito', 'change_carrito', 'delete_carrito'])
    permisos_pedido =  Permission.objects.filter(codename__in=['view_pedido', 'add_pedido', 'change_pedido', 'delete_pedido'])
    permisos_detalles_pedido =  Permission.objects.filter(codename__in=['view_detallepedido', 'add_detallepedido', 'change_detallepedido', 'delete_detallepedido'])
    
    # Asignar permisos a los grupos
    # Obtener todos los permisos disponibles
    all_permissions = Permission.objects.all()

    # Asignar todos los permisos al grupo de vendedores
    group_vendedor.permissions.set(permisos_carrito | permisos_item_carrito | permisos_pedido | permisos_detalles_pedido | permisos_producto | permisos_categoria)
    
    group_cliente.permissions.set(permisos_carrito | permisos_item_carrito | permisos_pedido | permisos_detalles_pedido )

    # Asignar los grupos a los usuarios correspondientes
    # Ejemplo: asumiendo que los usuarios se han creado previamente
    # usuario_vendedor.groups.add(group_vendedor)
    # usuario_cliente.groups.add(group_cliente)

# Llamar a la función para configurar grupos y permisos
configurar_grupos_y_permisos()
