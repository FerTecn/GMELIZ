"""
URL configuration for GanaderiaSoft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from catalogos import views

urlpatterns = [
    # path('homeCatalogos', views.homeCatalogos, name='homeCatalogos'),

    path('categoria/lista', views.categoriaList, name='categoriaList'),
    path('categoria/agregar', views.categoriaCreate, name='categoriaCreate'),
    path('categoria/editar/<int:pk>', views.categoriaUpdate, name='categoriaUpdate'),
    path('categoria/eliminar/<int:pk>', views.categoriaDelete, name='categoriaDelete'),

    path('producto/lista', views.productoList, name='productoList'),
    path('producto/agregar', views.productoCreate, name='productoCreate'),
    path('producto/editar/<int:pk>', views.productoUpdate, name='productoUpdate'),
    path('producto/eliminar/<int:pk>', views.productoDelete, name='productoDelete'),

    path('tienda/', views.tienda, name='tienda'),
    path('producto_agotado/', views.producto_agotado, name='producto_agotado'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('limpiar_carrito/', views.limpiar_carrito, name='limpiar_carrito'),
    
    path('agregar_producto/<int:producto_id>/', views.agregar_producto_carrito, name='agregar_producto_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('ver_pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('detalle_pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]
