from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .forms import CheckOutForm, UploadForm
from .models import Product

def home(request):
    template = 'product/home.html'
    products = Product.objects.all()
    form = UploadForm()
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload_form.save()
            messages.success(request=request, message="New Product Uploaded successfully")
            return render(request=request, template_name=template, context={'products': products})
        messages.error(request=request, message='Something went wrong')
        return render(request=request, template_name=template, context={'form': form})
    return render(request=request, template_name=template, context={'form': form,
                                                 'products': products})


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
        print(e)
        return HttpResponse({})


def add_to_cart(request):
    try:
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        cart = request.session.get('cart', {})
        if product_id not in cart.keys():
            print(f"{product_id} not found in {cart.keys()}")
            cart[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 1
            }
        else:
            cart[product_id]['quantity'] = int(cart[product_id]['quantity']) + 1
            print(cart[product_id]['price'], int(
                cart[product_id]['quantity']))
            cart[product_id]['price'] =\
                (int(cart[product_id]['price']) *
                 int(cart[product_id]['quantity']))

        request.session['cart'] = cart
        return JsonResponse({"message": "recevied"})
    except Product.DoesNotExist as e:
        messages.error(request=request, message="Item not added to cart, try again")
        return JsonResponse({"error": "No product found"}, status=404)

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

def check_out(request):
    form = CheckOutForm()
    session_data = request.session.get('cart', {})
    prices = [int(item.get('price')) for item in list(session_data.values())]
    product_sum = sum(prices)
    data = {
        'total_price': product_sum,
    }

    return render(request, 'product/checkout.html', {'data': data if data else None,
                                                     'form': form})

from allauth.socialaccount import adapter