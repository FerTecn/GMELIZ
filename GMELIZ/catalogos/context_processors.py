from .models import Carrito, Pedido

def carrito_count(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if carrito:
            return {'carrito_count': carrito.totalproductos}
    return {'carrito_count': 0}
