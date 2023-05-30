"""This module will contain utility functions to be used by the rest of the application"""
from math import pow

from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User, MatchHistory

def hello_world():
    '''Simple Hello World Function'''
    return "Hello World!"

# Will assume valid choice is passed into this
class player_choice:
    def __init__(self, username, choice):
        self.username = username
        self.choice = choice

# Function to calculate the Probability
# https://www.geeksforgeeks.org/elo-rating-algorithm/#
def Probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * pow(10, 1.0 * (rating1 - rating2) / 400))

def calculate_elo_change(Ra, Rb, winner):
    Pb = Probability(Ra, Rb)
    Pa = Probability(Rb, Ra)
    
    if (str(winner) == "1"):
        Ra = Ra + 30 * (1 - Pa)
        Rb = Rb + 30 * (0 - Pb)
 
    else:
        Ra = Ra + 30 * (0 - Pa)
        Rb = Rb + 30 * (1 - Pb)
 
    return (int(Ra),int(Rb))

def getUserRecordFromUsername(username):
    res = User.query.filter_by(username=username).first()
    if not res:
        return None
    return res

def getRecentMatchFromUsername(username):
    res = User.query.filter_by(username=username).first()
    if not res:
        return None
    most_recent_match = MatchHistory.query.filter(
        (MatchHistory.player_one_id == res.id) |
        (MatchHistory.player_two_id == res.id)
    ).order_by(MatchHistory.match_created.desc()).first()

    return most_recent_match
