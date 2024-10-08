from django.shortcuts import render, redirect
from store.models.product import Product 
from store.models.category import Category
from django.views import View
# Create your views here.



class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] -= 1
                else:
                    cart[product] += 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('index')
    def get(self , request):
        products = None
        
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        context = {
            'products': products,
            'categories': categories,

        }
        print("your are : ", request.session.get('email'))
        return render(request, 'index.html', context)


       

def orders(request):

    return render(request, 'orders/order.html')

