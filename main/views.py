from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
import json

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.all()
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category=category_filter)
    
    # Filter by user (My Products)
    filter_type = request.GET.get('filter')
    if filter_type == 'my' and request.user.is_authenticated:
        products = products.filter(user=request.user)
    
    context = {
        'product_list': products,
        'name': request.user.username,
        'last_login': request.session.get('last_login', 'Never'),
    }
    return render(request, 'main.html', context)

def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def detail_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "detail_product.html", context)

def show_xml(request):
    product_list = Product.objects.all() # Ambil semua data dari database
    xml_data = serializers.serialize("xml", product_list)  # covert ke format XML
    return HttpResponse(xml_data, content_type="application/xml") # kirim sebagai response XML

# def show_json(request):
#     product_list = Product.objects.all()
#     json_data = serializers.serialize("json", product_list)
#     return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
   try:
       product_item = Product.objects.filter(pk=product_id) # Ambil data berdasarkan id tertentu
       xml_data = serializers.serialize("xml", product_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist: # jika data tidak ditemukan
       return HttpResponse(status=404)

def show_json_by_id(request, product_id):
   try:
       product_item = Product.objects.get(pk=product_id)
       json_data = serializers.serialize("json", [product_item])
       return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def show_json(request):
    product_list = Product.objects.all()
    
    data = [
        {
            'id': product.id, 
            'name': product.name,
            'price': product.price, 
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
            'user': product.user.username, 
            'user_id': product.user.id if product.user else None,
        } 

        for product in product_list
    ]

    return JsonResponse(data, safe=False)

def get_product_detail_json(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'amount': getattr(product, 'amount', 0),
            'description': product.description,
            'category': product.category,
            'image': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': getattr(product, 'is_featured', False),
            'user_username': product.user.username,
            'date_added': product.date_added.isoformat() if hasattr(product, 'date_added') else '',
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    name = request.POST.get("name")
    price = request.POST.get("price")  # PASTIKAN INI ADA
    description = request.POST.get("description")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'
    user = request.user

    # Debug print
    print(f"Creating product: {name}, Price: {price}")

    new_product = Product(
        name=name, 
        price=price, 
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

def login_ajax(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = JsonResponse({'status': 'success', 'message': 'Login successful'})
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def register_ajax(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success', 
                'message': 'Your account has been successfully created! Redirecting to login...'
            })
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
@require_http_methods(["PUT", "POST"])
def edit_product_ajax(request, product_id):
    try:
        product = Product.objects.get(pk=product_id, user=request.user)
        
        # Parse JSON data
        data = json.loads(request.body)
        
        # Update product fields
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.category = data.get('category', product.category)
        product.thumbnail = data.get('thumbnail', product.thumbnail)
        product.is_featured = data.get('is_featured', product.is_featured)
        
        product.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product updated successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'category': product.category,
                'thumbnail': product.thumbnail,
                'is_featured': product.is_featured
            }
        })
        
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found or you do not have permission to edit it'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def delete_product_ajax(request, product_id):
    try:
        product = Product.objects.get(pk=product_id, user=request.user)
        product_name = product.name
        product.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Product "{product_name}" deleted successfully'
        })
        
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found or you do not have permission to delete it'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)