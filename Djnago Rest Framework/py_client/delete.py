import requests

product_id = input("Enter the id you want to delete? /n")
try:
    product_id = int(product_id)
except:
    product_id = None
    print(f'{product_id } not a valid id' )
    
if product_id:

    # endpoints="https://httpbin.org/anything"
    endpoints=f"http://localhost:8000/api/products/{product_id}/delete"
    get_respose = requests.delete(endpoints)
    # print(get_respose.text)
    print(get_respose.status_code, get_respose.status_code==204)