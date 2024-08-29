import requests
import json
# endpoints="https://httpbin.org/anything"
endpoints="http://localhost:8000/api/products/"

get_respose = requests.get(endpoints)
print(get_respose.text)
# print(get_respose.json())