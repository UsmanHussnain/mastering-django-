from django.shortcuts import render
from django.views import View
from store.models.product import Product




class Cart(View):

    def get(self, request ):
        
        ids = list(request.session.get('cart'))
        products = Product.get_product_by_id(ids)
        print(products)

        context = {'products': products}

        return render(request, 'cart.html', context)