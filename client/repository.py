import requests

__endpoint_url__ = "http://localhost:5000" #TODO: Change to GCE IP once that is stable

def login(username: str, password: str):
    return requests.post(__endpoint_url__ + "/login", {
        "username": username,
        "password": password
    })

def make_choice(username: str, choice: str):
    print(f"Making choice of: {choice}")
    return requests.post(__endpoint_url__ + "/report", {
        "username": username,
        "choice": choice
    })
