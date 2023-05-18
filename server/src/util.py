"""This module will contain utility functions to be used by the rest of the application"""
from math import pow

from werkzeug.security import generate_password_hash, check_password_hash

def hello_world():
    '''Simple Hello World Function'''
    return "Hello World!"

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