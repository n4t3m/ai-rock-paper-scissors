'''This module contains API calls for the RPS Game'''

from flask import Blueprint, session, abort, request, jsonify

from config import db
from src.util import hello_world
from src.decorators import login_required
from src.models import User, MatchHistory

rps_routes = Blueprint("rps_routes", __name__)

@rps_routes.route("/", methods=["GET"])
def hello_world_route():
    '''Simple Hello World API Call'''
    return hello_world()

@rps_routes.route("/register", methods=["POST"])
def register():
    '''Registration Route'''
    username = request.form.get("username")
    if not username:
        # print("Username Not Provided!")
        abort(400)
    password = request.form.get("password")
    if not password:
        # print("Password not Provided!")
        abort(400)

    try:
        # Create User in Database
        db.session.add(User(
            username=username,
            password=password,
        ))
        db.session.commit()
        return f"User {username} successfully created!"
    except:
        # this handles all potential errors, including duplicate usernames
        abort(500) # todo, figure out better way to handle this

# @rps_routes.route("/login", methods=["GET"])
# def login():
#     '''Simple "Login" Route for testing, log into psuedo Guest User'''
#     session['username']="Guest"
#     return "You have been logged in!"

@rps_routes.route("/login", methods=["POST"])
def login():
    '''Login Route'''
    username = request.form.get("username")
    if not username:
        # print("Username Not Provided!")
        abort(400)
    password = request.form.get("password")
    if not password:
        # print("Password not Provided!")
        abort(400)

    user_record = User.query.filter_by(username=username).first()

    if user_record and user_record.verify_password(password):
        session['username']=username
        return "You have been logged in!"

    return "Username/Password Combination Not Found"

@rps_routes.route("/logout", methods=["GET"])
def logout():
    '''Simple "Logout" Route'''
    if "username" in session:
        del session["username"]
        return "You have been logged out!"
    return abort(401)

@rps_routes.route("/auth_check", methods=["GET"])
@login_required
def protected_route():
    '''Simple Auth-Check Route'''
    return "You are authenticated!"

@rps_routes.route("/init_match", methods=["POST"])
def init_match():
    '''Registration Route'''

    playerOneID = request.form.get("player_one_id")
    if not playerOneID:
        abort(400)
    playerTwoID = request.form.get("player_two_id")
    if not playerTwoID:
        abort(400)

    # Ensure Player is not in Match Already
    res = MatchHistory.query.filter_by(player_one_id=playerOneID).first()
    if res:
        return "Player 1 Already In Match"
    res = MatchHistory.query.filter_by(player_two_id=playerTwoID).first()
    if res:
        return "Player 2 Already In Match"
    
    # TODO: Check to see if user reporting result was in match

    try:
        # Create User in Database
        m = MatchHistory(
            player_one_id=playerOneID,
            player_two_id=playerTwoID,
        )
        db.session.add(m)
        db.session.commit()
        return jsonify(
            match_id=m.match_id,
            match_creation_time=m.match_created
        )
    except:
        abort(500)

@rps_routes.route("/report_result", methods=["POST"])
def report_result_match():
    '''Match Status Route'''

    # TODO: Use Match ID for this route

    playerOneID = request.form.get("player_one_id")
    if not playerOneID:
        abort(400)
    playerTwoID = request.form.get("player_two_id")
    if not playerTwoID:
        abort(400)
    winner = str(request.form.get("winner"))
    if not winner or (winner!="1" and winner!="2"):
        print(winner)
        abort(400)

    # Ensure Match Exists
    res = MatchHistory.query.filter(
        db.or_(
            db.and_(MatchHistory.player_one_id==playerOneID, MatchHistory.player_two_id==playerTwoID),
            db.and_(MatchHistory.player_one_id==playerTwoID, MatchHistory.player_two_id==playerOneID)
        )).first()

    if not res:
        return "Match Not Found"
    
    # TODO: Check to see if user reporting result was in match
    print("here4")

    try:
        res.winner = winner
        db.session.commit()
        return jsonify(
            winner=res.winner,
            match_id=res.match_id,
        )
    except:
        abort(500)