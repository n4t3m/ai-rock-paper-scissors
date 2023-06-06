import requests

__endpoint_url__ = "http://localhost:5000" #TODO: Change to GCE IP once that is stable

def login(session, username: str, password: str) -> int:
    r = session.post(__endpoint_url__ + "/login", {
        "username": username,
        "password": password
    })
    return r.status_code

def register(session, username: str, password: str) -> int:
    r = session.post(__endpoint_url__ + "/register", {
        "username": username,
        "password": password
    })
    return (r.status_code, r.text)

def make_choice(session, choice: str):
    if choice not in ["rock", "paper", "scissors"]:
        return None
    print(f"Making choice of: {choice}")
    r = session.post(__endpoint_url__ + "/report", {
        "choice": choice
    })
    return r.status_code

def retrieve_stats(session):
    r = session.get(__endpoint_url__ + "/queuecheck")
    if not r:
        return None
    r = r.json()
    return r
