from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_image')
    prepopulated_fields = {'slug': ('name',)}

    def get_image(self, category):
        if category.image:
            return mark_safe(f'<img src="{category.image.url}" width="75px;">')
        return '-'
    get_image.short_description = 'Rasm'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_by', 'price', 'quantity', 'category', 'published', 'created', 'get_image')
    list_display_links = ('id', 'title')

    def get_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="75px;">')
        return '-'

    get_image.short_description = 'Rasmi'

    prepopulated_fields = {'slug': ('title',)}

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hex_value')
    list_display_links = ('id', 'name')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created', 'is_activ')
    list_editable = ('is_activ',)
    list_display_links = ('id', 'customer')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity','added')
    list_display_links = ('id', 'order', 'product')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name')
    list_display_links = ('id', 'user')

@admin.register(ShippinAddres)
class ShippingAddresAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'address', 'city', 'country', 'zip_code', 'phone', 'email')
    list_display_links = ('id', 'customer')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'shipping_address', 'photo')
    list_display_links = ('id', 'user')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating')
    list_display_links = ('id', 'user')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'product', 'created')
    list_display_links = ('id', 'author', 'text')


