import requests
from config import BASE_URL, HEADERS

response = requests.get(BASE_URL, headers=HEADERS)
print("Status Code:", response.status_code)
print(response.text[:500])