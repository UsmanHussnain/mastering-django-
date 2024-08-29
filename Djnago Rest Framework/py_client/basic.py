import requests

# endpoints="https://httpbin.org/anything"
endpoints="http://localhost:8000/api/"


get_respose = requests.post(endpoints, json={'title':'Usman', 'content':'abc', 'price':123})
print(get_respose.text)
# print(get_respose.status_code)
print(get_respose.json())