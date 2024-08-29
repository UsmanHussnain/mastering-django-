import requests

product_id = input("Enter the id you want to update?  ")
try:
    product_id = int(product_id)
except:
    product_id = None
    print(f'{product_id } not a valid id' )
    
if product_id:

    # endpoints="https://httpbin.org/anything"
    endpoints=f"http://localhost:8000/api/products/{product_id}/update/"

    data = {
        'title': 'Updated Usman Product',
        'price': 421
    }

    get_response = requests.put(endpoints, json=data)
    # print(get_respose.text)
    print(get_response.json())



