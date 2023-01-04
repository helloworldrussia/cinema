import requests


def get_response_info(response):
    print(response.status_code)
    print(response.json())


data = {
    "user": {
        "username": "user2",
        "email": "use@user.user",
        "password": "qweasdzxc"
    }
}

response = requests.post("http://127.0.0.1:8000/api/v1/registration/", json=data)
get_response_info(response)
