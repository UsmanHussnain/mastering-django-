from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from .forms import SuperuserCreationForm
from base.forms import OrderForm
from django.contrib.auth import get_user_model
from base.models import customuser , Order
from django.shortcuts import render, get_object_or_404, redirect
from base.models import Product, ProductImage, Category, Brand , Querries
from .forms import ProductForm, ProductImageForm , CategoryForm , BrandForm
import os


User = get_user_model()

# Create your views here.

def home(request):
    return render(request, 'base/home.html')


def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = get_user_model()
        user = customuser.objects.filter(models.Q(username=username) | models.Q(email=username)).first()
        if user is not None and user.is_superuser:
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user is not None:
                login(request, auth_user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('adminIndex')
            else:
                return render(request, 'adminpanel/adminLogin.html', {'error_message': 'Invalid username or password.'})
        else:
            return render(request, 'adminpanel/adminLogin.html', {'error_message': 'Only superusers can login.'})
    else:
        return render(request, 'adminpanel/adminLogin.html')


@login_required(login_url='adminLogin')
def adminIndex(request):
    category_count = Category.objects.count()
    brand_count = Brand.objects.count()
    product_count = Product.objects.count()
    orders = Order.objects.all().prefetch_related('orderitem_set__product')

    total_orders = orders.count()
    received_orders = orders.filter(status='Received').count()
    delivered_orders = orders.filter(status='Delivered').count()
    

    context = {
        'category_count': category_count,
        'brand_count': brand_count,
        'product_count': product_count,
        'orders': orders,
        'total_orders': total_orders,
        'received_orders': received_orders,
        'delivered_orders': delivered_orders,
    }
    return render(request, 'adminpanel/dashboard.html', context)


@login_required(login_url='adminLogin')
def adminLogout(request):
    logout(request)
    return redirect('home')



@login_required(login_url='adminLogin')
def uiElements(request):
    return render(request, 'adminpanel/ui.html')


@login_required(login_url='adminLogin')
def tabPanel(request):
    return render(request, 'adminpanel/tab-panel.html')


@login_required(login_url='adminLogin')
def charts(request):
    return render(request, 'adminpanel/chart.html')


@login_required(login_url='adminLogin')
def table(request):
    return render(request, 'adminpanel/table.html')


@login_required(login_url='adminLogin')
def forms(request):
    return render(request, 'adminpanel/form.html')


@login_required(login_url='adminLogin')
def blankpage(request):
    return render(request, 'adminpanel/blank.html')



@login_required(login_url='adminLogin')
def create_Super_User(request):
    if request.user.is_authenticated and request.user.is_superuser:
       
        if request.method == 'POST':
            form = SuperuserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=True)
                user.is_staff = True
                user.is_superuser = True
                user.is_verified = False  
                user.generate_verification_token()  
                
                customuser.send_email_verification(user)  
                user.save()
                return redirect('adminIndex')
        else:
            form = SuperuserCreationForm()
        return render(request, 'adminpanel/create_superuser.html', {'form': form})



@login_required(login_url='adminLogin')
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        image_form = ProductImageForm(request.POST, request.FILES)
        
        if product_form.is_valid() and image_form.is_valid():
            product = product_form.save(commit=False)
            product.save()
            
            image_instance = image_form.save(commit=False)
            image_instance.product = product  
            image_instance.save()

            return redirect('adminIndex') 
    else:
        product_form = ProductForm()
        image_form = ProductImageForm()
    
    context = {
        'product_form': product_form,
        'image_form': image_form,
    }
    return render(request, 'adminpanel/add_product.html', context)


@login_required(login_url='adminLogin')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-detail', pk=pk)
    else:
        form = ProductForm(instance=product)

    
    context = {
        'form': form, 
        'product': product

    }

    return render(request, 'adminpanel/edit_product.html', context)

@login_required(login_url='adminLogin')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = { 
        'product': product,

    }
    return render(request, 'adminpanel/product_detail.html', context)

@login_required(login_url='adminLogin')
def productList(request):
    products = Product.objects.all()
    user = request.user
    
    context = {

        'products': products,
        'user': user,
        
        }
    return render(request, 'adminpanel/productList.html', context)




@login_required(login_url='adminLogin')
def add_product_images_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        try:
            images = request.FILES.getlist('images')
            product = Product.objects.get(id=pk)
            for image in images:
                product_image = ProductImage.objects.create(
                    product=product,
                    image=image
                )
            return redirect('productList')  
        except Exception as e:
            print(e)
           
    return render(request, 'adminpanel/add_product_images.html')  


@login_required(login_url='adminLogin')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    for image in product.images.all():
        image_path = image.image.path
        if os.path.exists(image_path):
            os.remove(image_path)
        image.delete()
    product.delete()
    return redirect('productList')


@login_required(login_url='adminLogin')
def adminOrder(request):
    user = request.user
    orders = Order.objects.all().prefetch_related('orderitem_set__product')
    
    
    
    context = {
        'user': user,
        'orders': orders
        
    }
    return render(request, 'adminpanel/orders.html', context)

@login_required(login_url='adminLogin')
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('adminOrder') 
    else:
        form = OrderForm(instance=order)
    
    context = {
        'form': form,
        'order': order
    }
    return render(request, 'adminpanel/edit_order.html', context)




@login_required(login_url='adminLogin')
def category_detail(request):
    
    categories = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-detail')
    else:
        form = CategoryForm()
        
    context = {
        'form': form,
        'categories' : categories,
    }
    
    return render(request, 'adminpanel/CategoryDetail.html', context)


@login_required(login_url='adminLogin')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category.delete()
        return redirect('category-detail')
    
    
    
@login_required(login_url='adminLogin')
def brand_detail(request):
    
    brands = Brand.objects.all()
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand-detail')
    else:
        form = BrandForm()
        
    context = {
        'form': form,
        'brands' : brands,
    }
    
    return render(request, 'adminpanel/BrandDetail.html', context)

@login_required(login_url='adminLogin')
def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == "POST":
        brand.delete()
        return redirect('brand-detail')
    
    
    


@login_required(login_url='adminLogin')
def list_querries(request):
    querries = Querries.objects.all()
    user = request.user
    context = {
        'user': user,
        'querries': querries
    }
    return render(request, 'adminpanel/Querries.html', context)


@login_required(login_url='adminLogin')
def delete_querry(request, pk):
    querry = get_object_or_404(Querries, pk=pk)
    if request.method == "POST":
        querry.delete()
        return redirect('querries')