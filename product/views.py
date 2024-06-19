from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .forms import UploadForm
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
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload_form.save()
            messages.success(request, "New Product Uploaded successfully")
            return redirect('product:home')
        messages.error(request, 'Something went wrong')
        return render(request, 'product/home.html', {'form': form})
    return render(request=request, template_name=template, context={'form': form})


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
                    str(int(cart[product_id]['price']) + int(product.price))

        request.session['cart'] = cart
        return JsonResponse({"message": "recevied"})
    except Product.DoesNotExist as e:
        messages.error(request=request, message="Item not added to cart, try again")
        return JsonResponse({"error": "No product found"}, status=404)


def view_cart(request):
    template = 'product/cart.html'
    cart = request.session.get('cart')
    print(cart)
    return render(request=request, template_name=template, context={'cart': cart.values()})

def check_out(request):
    return HttpResponse({"message": "recieved"})