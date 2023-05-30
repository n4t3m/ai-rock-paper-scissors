"""This module will contain utility functions to be used by the rest of the application"""
from datetime import datetime
from math import pow

from flask import g, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from config import db
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

def record_tie(p1username, p2username):
    '''no winner, no elo calculation'''
    p1 = User.query.filter_by(username=p1username).first()
    p2 = User.query.filter_by(username=p2username).first()

    m = MatchHistory(
        player_one_id=p1.id,
        player_two_id=p2.id,
    )

    m.player_one_final_elo, m.player_two_final_elo = m.player_one_initial_elo, m.player_two_initial_elo
    m.player_one_ack = m.player_two_ack = True
    m.winner = "3"
    m.match_created = datetime.now()

    db.session.add(m)
    db.session.commit()

def record_win(p1username, p2username, winner):
    '''winner==1 is p1win, winner==2 is p2win'''
    p1 = User.query.filter_by(username=p1username).first()
    p2 = User.query.filter_by(username=p2username).first()

    m = MatchHistory(
        player_one_id=p1.id,
        player_two_id=p2.id,
    )

    m.player_one_final_elo, m.player_two_final_elo = calculate_elo_change(m.player_one_initial_elo, m.player_two_initial_elo, str(winner))
    User.query.filter_by(id=p1.id).first().elo = m.player_one_final_elo
    User.query.filter_by(id=p2.id).first().elo = m.player_two_final_elo
    m.player_one_ack = m.player_two_ack = True
    m.winner = str(winner)
    m.match_created = datetime.now()

    db.session.add(m)
    db.session.commit()

def determine_rps_winner(p1_choice, p2_choice):
    '''RPS. Return 1 if p1win. Return 2 is p2win. Return 0 if tie.'''
    if p1_choice == p2_choice:
        return 3

    if p1_choice == "rock":
        if p2_choice == "paper":
            return 2
        elif p2_choice == "scissors":
            return 1

    if p1_choice == "paper":
        if p2_choice == "rock":
            return 1
        elif p2_choice == "scissors":
            return 2

    if p1_choice == "scissors":
        if p2_choice == "rock":
            return 2
        elif p2_choice == "paper":
            return 1

    return None

def playMatches(app):
    with app.app_context():
        while app.config['QUEUE'].qsize() >= 2:
            p1 = app.config['QUEUE'].get()
            p2 = app.config['QUEUE'].get()

            res = determine_rps_winner(p1.choice, p2.choice)

            if not res:
                print("Could not determine RPS Winner")
                return # TODO: log if invalid result is sent
            if res == 3:
                # Tie, Record Match
                record_tie(p1.username, p2.username)
                pass
            elif res==1:
                # P1 Wins
                record_win(p1.username, p2.username, "1")
            else:
                # P2 Wins
                record_win(p1.username, p2.username, "2")
