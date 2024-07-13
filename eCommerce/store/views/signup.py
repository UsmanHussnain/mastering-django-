from django.shortcuts import render, redirect
from store.models.customer import Customer
from django.contrib.auth.hashers import make_password
from django.views import View


class signup(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        
        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
        error_message = self.validateCustomer(customer)

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone' : phone,
            'email' : email,
            'password' :  password,
        }

        # Saving Form
        if (not error_message):
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('index')
        else:
            context = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html',context)

    def validateCustomer(self , customer):
        error_message = None

    # Validation
        if (not customer.first_name):
            error_message = "First Name Required"
        elif len(customer.first_name) < 3:
            error_message = "First Name Must be greater than 3 Character"
        elif (not customer.last_name):
            error_message = "Last Name Required"
        elif len(customer.last_name) < 3:
            error_message = "Last Name Must be greater than 3 Character"
        elif (not customer.phone):
            error_message = "Phone Number Required"
        elif len(customer.phone) < 11:
            error_message = "Phone Number Must be greater or equal to 11 Character"
        elif (not customer.password):
            error_message = "Password Required"
        elif len(customer.password) < 4:
            error_message = "Password Must be greater or equal to 8 Character"
        elif customer.isExists():
            error_message = "Email Already Exists"
        return error_message
