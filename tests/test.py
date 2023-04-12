import requests

response = requests.post(
    url='http://127.0.0.1:8000/service-account',
    json={
        "name": "eric",
        "namespace": "default",
    }
)

print(response.text)