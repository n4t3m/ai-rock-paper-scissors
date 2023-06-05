import requests

__endpoint_url__ = "http://localhost:5000" #TODO: Change to GCE IP once that is stable

def login(session, username: str, password: str) -> int:
    r = session.post(__endpoint_url__ + "/login", {
        "username": username,
        "password": password
    })
    return r.status_code

def make_choice(session, choice: str):
    if choice not in ["rock", "paper", "scissors"]:
        return None
    print(f"Making choice of: {choice}")
    r = session.post(__endpoint_url__ + "/report", {
        "choice": choice
    })
    return r.status_code
