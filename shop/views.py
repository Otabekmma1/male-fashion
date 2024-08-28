from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import ListView, FormView, CreateView, View
from .utils import CartAuthenticatedUser
import stripe
from male_fashion import settings
from django.urls import reverse, reverse_lazy
from .forms import *
from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
import requests


#--------------------------- USER -------------------------------------------------
class UserLogin(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

class UserRegister(CreateView):
    template_name = 'user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
        return response if form.is_valid() else render(self.request, self.template_name, {'form': form})


@login_required
def logout_user(request):
    try:
        logout(request)
        return redirect('login')
    except Exception:
        return redirect('login')


@login_required(login_url='login')
def user_profile(request):
    profile_info = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(customer=profile_info.customer, is_activ=False)
    ctx = {
        'profile_info': profile_info,
        'orders': orders
    }
    return render(request, 'user/profile.html', context=ctx)


@login_required(login_url='login')
def delete_profile(request):
    user = User.objects.get(username=request.user.username)
    user.delete()
    return redirect('login')


#----------------------------------------- ENDUSER -------------------------------------------------



def index(request):
    if request.user.is_authenticated:
        return render(request, 'pages/index.html')
    else:
        return redirect('login')


def shop(request, category_id=None, size_id=None):
    products = Product.objects.filter(published=True)

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    if size_id:
        size = get_object_or_404(Size, id=size_id)
        products = products.filter(size=size)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'page_obj': page_obj,
    }
    return render(request, 'pages/shop.html', ctx)


def blog(request):
    return render(request, 'pages/blog.html')


def blog_detail(request):
    return render(request, 'pages/blog-details.html')


def contact(request):
    return render(request, 'pages/contact.html')





def product_detail_by_slug(request, slug):
    product = Product.objects.get(slug=slug, published=True)
    related_products = Product.objects.filter(published=True, category=product.category)
    rating = Rating.objects.filter(product=product, user=request.user).first()
    comments = Comments.objects.filter(product=product)

    if request.method == 'POST':
        author = User.objects.get(username=request.user.username)
        text = request.POST.get('text')
        if all([author, text]):
            Comments.objects.create(
                author=author,
                text=text,
                product=product
            )
    ctx = {
        'product': product,
        'comments': comments,
        'user_rating': rating.rating if rating else 0,
        'related_products': related_products

    }
    return render(request, 'pages/shop-details.html', ctx)


class SortingProductList(ListView):
    model = Product
    template_name = 'pages/shop.html'
    paginate_by = 9

    def get_queryset(self):
        key_name = self.kwargs['key_name']
        queryset = Product.objects.filter(filter_price=key_name, published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context




#------------------------------------- CART -------------------------------------------------

@login_required(login_url='login')
def check(request):
    return render(request, 'pages/checkout.html')

@login_required(login_url='login')
def cart(request):
    return render(request, 'pages/shopping-cart.html')


@login_required(login_url='login')
def to_cart(request, product_id, action):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')

        try:
            color = Color.objects.get(id=color_id)
        except Color.DoesNotExist:
            color = None
        try:
            size = Size.objects.get(id=size_id)
        except Size.DoesNotExist:
            size = None
        CartAuthenticatedUser(request, product_id, action, quantity=quantity, size=size, color=color)
    else:
        quantity = 1
        CartAuthenticatedUser(request, product_id, action, quantity)

    current_page = request.META.get('HTTP_REFERER', 'index')
    return redirect(current_page)

@login_required(login_url='login')
def delete_product_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        order = cart_info['order']
        order_product = order.orderproduct_set.get(product_id=product_id)
        product = order_product.product
        product.quantity += order_product.quantity
        product.save()
        order_product.delete()
        return redirect('cart')


def create_stripe_line_items(order_products):
    line_items = []
    for order_product in order_products:
        line_item = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': order_product.product.title,
                },
                'unit_amount': int(order_product.product.price * 100)
            },
            'quantity': order_product.quantity
        }
        line_items.append(line_item)
    return line_items


def create_shipping_address(request, order):
    shipping_address = ShippinAddres.objects.create(
        customer=order.customer,
        order=order,
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        country=request.POST.get('country'),
        zip_code=request.POST.get('zip_code'),
        phone=request.POST.get('phone'),
        email=request.POST.get('email')
    )

    user_profile = UserProfile.objects.get(user=order.customer.user)
    user_profile.shipping_address = shipping_address
    user_profile.save()

def format_order_info(order, order_products):
    order_info = (f"Mijoz: {order.customer.first_name} {order.customer.last_name}\n"
                  f"Zakaz raqami: {order.id}\n "
                  f"Umumiy narxi: ${order.get_cart_total_price}\n "
                  f"Mahsulotlar soni: {order.get_cart_total_quantity}\n\n"
                  f"Buyurtma mahsulotlari:\n")
    for count, order_product in enumerate(order_products, start=1):
        size_info = f"{', '.join(size.name for size in order_product.size.all())}" if order_product.size.exists() else "-"
        color_info = f"{', '.join(color.name for color in order_product.color.all())}" if order_product.color.exists() else "-"
        order_info += (f"{count}. Mahsulot nomi: {order_product.product.title}\n"
                       f"Soni: {order_product.quantity}\n"
                       f"Narxi: ${order_product.product.price}\n"
                       f"O'lcham: {size_info}\n"
                       f"Rangi: {color_info}\n"
                       f"Umumiy narx: ${order_product.get_cart_price}\n\n")
    return order_info


@login_required(login_url='login')
def create_checkout_sessions(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    order = cart_info['order']
    order_products = cart_info['order_products']

    line_items = create_stripe_line_items(order_products)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('profile')),
        cancel_url=request.build_absolute_uri(reverse('profile')),
    )

    if request.method == 'POST':
        create_shipping_address(request, order)

    order.is_activ = False
    order.save()

    order_info = format_order_info(order, order_products)
    send_order_info_to_telegram_bot(order_info)

    return redirect(session.url, 303)


def send_order_info_to_telegram_bot(order_info):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": order_info}
    requests.post(url, params=params)

@login_required(login_url='login')
def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        Rating.objects.filter(product=product, user=request.user).delete()
        product.rating_set.create(user=request.user, rating=rating)
    return redirect('product_detail', slug=product.slug)

