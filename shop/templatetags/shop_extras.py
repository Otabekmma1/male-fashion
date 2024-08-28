from django import template
from ..models import *
from ..utils import CartAuthenticatedUser

register = template.Library()

@register.simple_tag()
def all_products():
    return Product.objects.filter(published=True)

@register.simple_tag()
def all_categories():
    return Category.objects.all()

@register.simple_tag()
def all_sizes():
    return Size.objects.all()

@register.simple_tag()
def get_total_cart_quantity(request):
    cart_info = CartAuthenticatedUser(request).get_cart_info()
    return cart_info['cart_total_quantity']

@register.simple_tag()
def get_order_products(request):
    cart_info = CartAuthenticatedUser(request).get_cart_info()
    return cart_info['order_products']

@register.simple_tag()
def get_total_price(request):
    cart_info = CartAuthenticatedUser(request).get_cart_info()
    return cart_info['cart_total_price']

