from .models import *
from django.contrib.auth.models import User

class CartAuthenticatedUser:
    def __init__(self, request, product_id=None, action=None, quantity=1, color=None, size=None):
        self.request = request
        self.quantity = quantity
        self.color = color
        self.size = size

        if product_id and action:
            self.add_or_delete(product_id, action)

    def get_cart_info(self):
        user = User.objects.get(id=self.request.user.id)
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )
        user_profile = UserProfile.objects.get(user=self.request.user)
        user_profile.customer = customer
        user_profile.save()

        order, created = Order.objects.get_or_create(
            customer=customer,
            is_activ=True
        )

        order_products = order.orderproduct_set.all()

        cart_total_price = order.get_cart_total_price
        cart_total_quantity = order.get_cart_total_quantity

        return {
            'order': order,
            'order_products': order_products,
            'cart_total_price': cart_total_price,
            'cart_total_quantity': cart_total_quantity,
        }

    def add_or_delete(self, product_id, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(id=product_id)

        order_product, created = OrderProduct.objects.get_or_create(
            order=order,
            product=product
        )

        if action == 'add' and product.quantity >= self.quantity:
            order_product.quantity += self.quantity
            product.quantity -= self.quantity
            if self.color:
                order_product.color.add(self.color)
            if self.size:
                order_product.size.add(self.size)

        if action == 'delete' and order_product.quantity >= self.quantity:
            order_product.quantity -= self.quantity
            product.quantity += self.quantity

        order_product.save()
        product.save()

        if order_product.quantity <= 0:
            order_product.delete()
