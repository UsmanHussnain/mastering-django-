from django.contrib.auth import login , logout , get_user_model
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import customuser , Product, Category, Brand, OrderItem, Order , CustomerReview
from .forms import SignupForm, CustomAuthenticationForm, OrderForm , CustomerReviewForm, ProfileUpdateForm , QuerriesForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm 
from django.core.paginator import Paginator
import random
from django.db.models import Count
from django.db.models import Q
User = get_user_model()

default_user_id = User.id


def search(request):
    query = request.GET.get('query', '')
    price_range = request.GET.get('price')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()

    if price_range:
        try:
            min_price, max_price = map(int, price_range.split('-'))
            products = products.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass 

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = Category.objects.annotate(product_count=Count('product'))
    brands = Brand.objects.annotate(product_count=Count('product'))

    context = {
        'products': products,
        'query': query,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'base/products.html', context)


@login_required(login_url='login')
def index_view(request):
    return render(request, 'base/baseIndex.html')

def home(request):
    categories = Category.objects.all()
    recent_products = {category: Product.objects.filter(category=category).order_by('-created_at')[:5] for category in categories}
    
    featured_products = {}
    for category in categories:
        products = list(Product.objects.filter(category=category))
        if products:
            featured_products[category] = random.choice(products)
    
    reviews = CustomerReview.objects.all()
    
    context = {
        'categories': categories,
        'recent_products':recent_products,
        'featured_products': featured_products,
        'reviews' : reviews,
    }
    
    return render(request, 'base/home.html', context)



def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Welcome, {user.first_name +" "+ user.last_name}!')
                return redirect('home') 
            else:
                messages.error(request, 'You must verify your email address before logging in.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'base/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            try:
                existing_email_user = customuser.objects.get(email=email)
                messages.error(request, 'Email Already Exist')
                return render(request, 'base/signup.html', {'form': form})

            except User.DoesNotExist:
                pass 
            try:
                existing_username_user = customuser.objects.get(username=username)
                messages.error(request, 'Username Already Exist')
                return render(request, 'base/signup.html', {'form': form})

            except User.DoesNotExist:
                pass  

            user = form.save(commit=False)
            user.is_verified = False  
            user.save()

            User.send_email_verification(user)
            messages.success(request, 'Account created successfully! Please verify your email address.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'base/signup.html', {'form': form})

def verify_email(request, token):
    user = get_object_or_404(customuser, verification_token=token)

    if not user.is_verified:
        user.is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified successfully. You can now log in.')
    if user.is_superuser:
        return redirect('adminLogin') 
    else:
        return redirect('login')  
 


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile_detail(request):
    user = request.user
    profile_pic_url = user.profile_pic.url if user.profile_pic else None
    context = {
        'user': user,
        'profile_pic_url': profile_pic_url, 
    }
    return render(request, 'base/profile_detail.html', context)



@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile-detail') 
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'base/change_password.html', {'form': form})




# Template Implementation

def products(request):
    category_id = request.GET.get('category')
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, is_active=True)
    else:
        products = Product.objects.filter(is_active=True)
    
    categories = Category.objects.all()
    brands = Brand.objects.all()
    brands = Brand.objects.annotate(product_count=Count('product'))
    
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'base/products.html', context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    reviews = CustomerReview.objects.filter(product=product) 
    brands = Brand.objects.annotate(product_count=Count('product'))
    count = reviews.count()
    
    review_form = CustomerReviewForm(initial={'product': product})

    if 'cart' not in request.session:
        request.session['cart'] = {}

    if request.method == 'POST':
        if 'profession' in request.POST and 'review' in request.POST:
            review_form = CustomerReviewForm(request.POST)
            if review_form.is_valid():
                new_review = review_form.save(commit=False)
                new_review.user = request.user
                new_review.product = product
                new_review.save()
                return redirect('product_detail', id=product.id)
        else:
            product_id = str(request.POST.get('product'))
            add = request.POST.get('add')
            remove = request.POST.get('remove')
            cart = request.session['cart']

            quantity = cart.get(product_id, 0)

            if add:
                cart[product_id] = quantity + 1
            elif remove:
                if product_id in cart:
                    if quantity <= 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity - 1

            request.session['cart'] = cart

    

    context = {
        'product': product,
        'products': products,
        'categories': categories,
        'brands': brands,
        'related_products': related_products,
        'reviews': reviews,
        'count': count,
        'review_form': review_form,
    }
    return render(request, 'base/product-detail.html', context)


def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_category': category,
    }
    return render(request, 'base/products_by_category.html', context)

def products_by_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    products = Product.objects.filter(brand=brand)
    categories = Category.objects.all()
    brands = Brand.objects.annotate(product_count=Count('product'))

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'base/products.html', context)


def cart(request):
    if request.method == 'POST':
        product_id = str(request.POST.get('product'))
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})
        quantity = cart.get(product_id, 0)
        wishlist = request.session.get('wishlist', {})
        if product_id in wishlist:
            del wishlist[product_id]
            request.session['wishlist'] = wishlist

        if remove:
            if product_id in cart:
                if quantity <= 1:
                    cart.pop(product_id)
                else:
                    cart[product_id] = quantity - 1
        else:
            cart[product_id] = quantity + 1 if quantity else 1

        request.session['cart'] = cart
        
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']
    ids = list(cart.keys())
    products = Product.get_products_by_id(ids)
    context = {
        'products': products,
        'cart': cart,  
    }
    return render(request, 'base/cart.html', context)


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True

@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            cart = request.session.get('cart', {})
            products = Product.objects.filter(id__in=cart.keys())

            for product in products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart[str(product.id)],
                    user=request.user
                )

            clear_cart(request)
            return redirect('order_confirmation')
    else:
        form = OrderForm()

    return render(request, 'base/checkout.html', {'form': form})



def order_confirmation(request):
    return render(request, 'base/order_confirmation.html')



def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.session.get('wishlist', {})
    wishlist[str(product_id)] = True
    request.session['wishlist'] = wishlist
    return redirect('wishlist')

def remove_from_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        wishlist = request.session.get('wishlist', {})
        if product_id in wishlist:
            del wishlist[product_id]
        request.session['wishlist'] = wishlist
    return redirect('wishlist')

def wishlist(request):
    wishlist = request.session.get('wishlist', {})

    products = []
    for product_id in wishlist.keys():
        try:
            product = Product.objects.get(id=product_id)
            products.append(product)
        except Product.DoesNotExist:
            continue

    context = {
        'wishlist': products
    }
    return render(request, 'base/wishlist.html', context)


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    
    profile_pic_url = user.profile_pic.url if user.profile_pic else None  

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('my-account')
    else:
        profile_form = ProfileUpdateForm(instance=user)
    
    
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile-detail') 
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = PasswordChangeForm(request.user)
    
    
    orders = Order.objects.filter(user=user).prefetch_related('orderitem_set__product')    
    
    context = {
        'user': user,
        'profile_pic_url': profile_pic_url, 
        'orders': orders,
        'profile_form': profile_form,
        'password_form':password_form,
        
    }
    return render(request, 'base/my-account.html', context)


def contactUs(request):
    user = request.user
    if request.method == 'POST':
        form = QuerriesForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.user = user 
            query.save()
            messages.success(request, 'Your query has been submitted successfully!')
            return redirect('contactUs')
    else:
        form = QuerriesForm()

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'base/contactUs.html', context)
