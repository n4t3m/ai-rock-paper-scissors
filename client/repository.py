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
    return r.status_code, r.text

def make_choice(session, choice: str):
    if choice not in ["rock", "paper", "scissors"]:
        return None
    print(f"Making choice of: {choice}")
    r = session.post(__endpoint_url__ + "/report", {
        "choice": choice
    })
    return r.status_code

def logout(session):
    r = session.get(__endpoint_url__ + "/logout")

    return r.status_code, r.text

def get_sats(session):
    r = session.get(__endpoint_url__ + "/match/stats")
    return r.json()
    # return {
    # "losses": 1,
    # "matches": [
    #     {
    #         "final_elo": 1028,
    #         "id": "37001244278e4b94b220d0592a44bf09",
    #         "opponent_name": "nano_two",
    #         "result": "Win",
    #         "timestamp": "Mon, 05 Jun 2023 10:46:28 GMT",
    #     },
    #     {
    #         "final_elo": 1015,
    #         "id": "28104c36c6de43bb9267adf6fa568a18",
    #         "opponent_name": "nano_two",
    #         "result": "Tie",
    #         "timestamp": "Mon, 05 Jun 2023 10:46:13 GMT",
    #     },
    #     {
    #         "final_elo": 1015,
    #         "id": "5af82929fe4a4c118ddfd905c7891f4d",
    #         "opponent_name": "nano_two",
    #         "result": "Tie",
    #         "timestamp": "Mon, 05 Jun 2023 10:45:58 GMT",
    #     },
    #     {
    #         "final_elo": 1015,
    #         "id": "a4dd92ee0a394a02a529afb8a8e7f051",
    #         "opponent_name": "nano_two",
    #         "result": "Win",
    #         "timestamp": "Mon, 05 Jun 2023 10:45:23 GMT",
    #     },
    # ],
    # "ties": 2,
    # "wins": 2,
    # }

