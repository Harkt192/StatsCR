import requests


a = requests.post("http://127.0.0.1:8001/api/jwt/login",
                  {
                      "username": "harktreallife@gmail.com",
                      "password": "qwerty"
                  }
                  )
print(a.json())
b = requests.get("http://127.0.0.1:8001/api/jwt/users/me")
print(b)