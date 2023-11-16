#richiama per settings generale tutta app

from .cart import Cart

def cart(request):
    return {'cart':Cart(request)}

