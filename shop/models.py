from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nomi')
    '''Masalan: #FFFFFF'''
    hex_value = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=10, verbose_name='Nomi')

    def __str__(self):
        return self.name

FILTER_PRICE = {
    '0': '$0-50',
    '50': '$50-100',
    '100': '$100-200',
    '200': '$200-500',
    '500': '$500 +'
}


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoriya')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Sarlavha')
    author = models.CharField(max_length=255, default='admin', verbose_name='Muallif')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', default='products/default.jpg')
    price = models.FloatField(verbose_name='Narxi')
    filter_price = models.CharField(max_length=20, choices=FILTER_PRICE, null=True)
    quantity = models.IntegerField(default=0, verbose_name='Mahsulot soni')
    color = models.ManyToManyField(Color, verbose_name='Ranglar', null=True, blank=True)
    size = models.ManyToManyField(Size, verbose_name='Olchamlar', null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, max_length=255)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated = models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')
    sku = models.CharField(max_length=12, unique=True, verbose_name='SKU', blank=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100, null=True, default='')
    last_name = models.CharField(max_length=100, null=True, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_activ = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer}"

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_cart_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity




class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    size = models.ManyToManyField(Size, blank=True)
    color = models.ManyToManyField(Color, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title}"

    @property
    def get_cart_price(self):
        total_price = self.quantity * self.product.price
        return total_price




class ShippinAddres(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=14)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name}"


class Comments(models.Model):
    author = models.CharField(max_length=100, verbose_name="Muallif")
    text = models.TextField(verbose_name="Izoh")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.title}: {self.rating}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippinAddres, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to='profile/', default='profile/default.jpg')

    def __str__(self):
        return f"{self.user.username}"