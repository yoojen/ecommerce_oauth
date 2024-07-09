from django.http import JsonResponse
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from django.core.cache import cache
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CheckOutForm, UploadForm
from .models import Order, Product
from .decorators import is_admin, has_placed_order, is_not_admin

def home(request):
    template = 'product/home.html'
    if cache.get("products", None):
        products = cache.get("products")
    else:
        products = Product.objects.all()
        cache.set("products", products)
        print("not from cache")
    return render(request=request, template_name=template, context={'products': products})

@is_admin
@login_required
def add_product(request):
    template = 'product/add_product.html'
    form = UploadForm()
    try:
        if request.method == 'POST':
            upload_form = UploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                upload_form.save()
                messages.success(request, "New Product Uploaded successfully")
                return redirect('product:home')
            else:
                messages.error(request, 'Something went wrong')
                return render(request, 'product/home.html', {'form': form})
        return render(request=request, template_name=template, context={'form': form})
    except Exception as e:
        return HttpResponse(str(e))

@is_not_admin
def add_to_cart(request):
    try:
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        cart = request.session.get('cart', {})
        if product_id not in cart.keys():
            cart[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 1
            }
        else:
            cart[product_id]['quantity'] = int(cart[product_id]['quantity']) + 1
            cart[product_id]['price'] =\
                (int(cart[product_id]['price']) *
                 int(cart[product_id]['quantity']))

        request.session['cart'] = cart
        return JsonResponse({"message": "recevied"})
    except Product.DoesNotExist as e:
        messages.error(request=request, message="Item not added to cart, try again")
        return JsonResponse({"error": "No product found"}, status=404)

@is_not_admin
def view_cart(request):
    template = 'product/cart.html'
    cart = request.session.get('cart', {})
    products_to_remove = []
    for product in cart.keys():
        product_from_db = Product.objects.filter(id=int(product)).first()
        if not product_from_db:
            products_to_remove.append(product)
    for product in products_to_remove:
        del request.session['cart'][product]
    request.session.modified = True

    return render(request=request, template_name=template, 
                  context={'cart': request.session['cart'].values() if cart else None})
@login_required
def check_out(request):
    c_form = CheckOutForm()
    session_data = request.session.get('cart', {})
    prices = [int(item.get('price')) for item in list(session_data.values())]
    product_sum = sum(prices)
    if product_sum == 0:
        messages.warning(request, "Place order before checkout")
        return render(request, 'product/checkout.html', {'data': 0,
                                                         'c_form': c_form})
    data = {
        'total_price': product_sum,
    }

    if request.method == 'POST':
        c_form = CheckOutForm(request.POST)
        if c_form.is_valid():
            province = c_form.cleaned_data["province"]
            district = c_form.cleaned_data["district"]
            sector = c_form.cleaned_data["sector"]
            amount_payed = c_form.cleaned_data["amount_payed"]
            payment_method = c_form.cleaned_data["payment_method"]
            # Process payment provider transactions
            order, placed = Order.objects.get_or_create(user=request.user, province=province, district=district,
                                                        sector=sector, amount_payed=amount_payed, payment_method=payment_method)
            if placed:
                request.session['cart'] = {}
                request.session.modified = True
                data = {}
                messages.success(request, "Order Placeed successfully")
                send_mail("Order information", f"{request.build_absolute_uri() } \
                    want to inform you that your order has been placed successfully.\
                    It may take up two 24 hours to get your order dispatched.\
                    Thank your working with us!", settings.DEFAULT_FROM_EMAIL, ["yoojen28@gmail.com"]
                )
            else:
                messages.error("order not placed")
        else:
            messages.error(request, "Something went wrong")
    return render(request, 'product/checkout.html', {'data': data if data else None,
                                                     'c_form': c_form})

@has_placed_order
@login_required
def orders(request):
    from django.shortcuts import get_list_or_404
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).all()
        return HttpResponse({"message": str(orders)})
    else:
        return HttpResponse({"message": "error"})