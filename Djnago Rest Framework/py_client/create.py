import requests
import json
# endpoints="https://httpbin.org/anything"
endpoints="http://localhost:8000/api/products/"

data = {
    'title': 'Mixin View Method',
    'content': 'Content Created',
    'price': 123
}


get_respose = requests.post(endpoints, json=data)
# print(get_respose.text)
print(get_respose.json())