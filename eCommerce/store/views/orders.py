from django.shortcuts import render, redirect
from django.views import View
from store.models.product import Product
from store.models.orders import Order
from store.models.customer import Customer




class OrderView(View):

    def get(self, request):
        customer = request.session.get('customer')
        if customer:
            orders = Order.get_orders_by_customer(customer)
        else:
            orders = []
        context = {'orders': orders}
        return render(request, 'orders.html', context)

    