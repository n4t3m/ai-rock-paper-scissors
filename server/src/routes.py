'''This module contains API calls for the RPS Game'''

from flask import Blueprint, session, abort, request, jsonify, g, current_app

from config import db
from src.util import (
    hello_world,
    calculate_elo_change,
    get_matches_from_username,
    get_user_from_username,
    PlayerChoice,
    get_recent_match_data
)
from src.decorators import login_required
from src.models import User, MatchHistory

rps_routes = Blueprint("rps_routes", __name__)

@rps_routes.before_request
def before_request():
    '''Middleware, setup global matchmaking queue'''
    g.matchmaking_queue = current_app.config['QUEUE']

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
        abort(400, "Username not Provided")
    password = request.form.get("password")
    if not password:
        # print("Password not Provided!")
        abort(400, "Password not Provided")

    if len(username) < 4:
        abort(400, "Requested username is too short.")
    if len(username) > 32:
        abort(400, "Requested username is too long.")
    if len(password) < 6:
        abort(400, "Requested password is too short")
    if len(password) > 256:
        abort(400, "Requested password is too long")

    try:
        # Create User in Database
        db.session.add(User(
            username=username,
            password=password,
        ))
        db.session.commit()
        return f"User {username} successfully created!"
    except Exception:
        # this handles all potential errors, including duplicate usernames
        abort(500, "An error has occured.") # todo, figure out better way to handle this

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

    #if "username" in session:
        #abort(400, "You are already logged in!")

    user_record = User.query.filter_by(username=username).first()

    if user_record and user_record.verify_password(password):
        session['username']=username
        return "You have been logged in!"

    return abort(400, "Username/Password Combination Not Found")

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

    player_one_id = request.form.get("player_one_id")
    if not player_one_id:
        abort(400)
    player_two_id = request.form.get("player_two_id")
    if not player_two_id:
        abort(400)

    # Ensure Player is not in Match Already

    res = MatchHistory.query.filter(
        db.and_(
            db.or_(
        MatchHistory.player_one_id==player_one_id,
        MatchHistory.player_two_id==player_one_id
        ),
            MatchHistory.winner=="0"
        )).first()
    if res:
        return "Player 1 Already In Match"

    res = MatchHistory.query.filter(
        db.and_(
            db.or_(
        MatchHistory.player_two_id==player_two_id,
        MatchHistory.player_two_id==player_two_id
        ),
            MatchHistory.winner=="0"
        )).first()
    if res:
        return "Player 2 Already In Match"

    #try:
        # Create User in Database
    match_object = MatchHistory(
        player_one_id=player_one_id,
        player_two_id=player_two_id,
    )
    db.session.add(match_object)
    db.session.commit()
    return jsonify(
        match_id=match_object.match_id,
        match_creation_time=match_object.match_created
        )
    ##except:
        #abort(500)

@rps_routes.route("/report_result", methods=["POST"])
@login_required
def report_result_match():
    '''Match Status Route'''

    # TODO: Use Match ID for this route

    player_one_id = request.form.get("player_one_id")
    if not player_one_id:
        abort(400)
    player_two_id = request.form.get("player_two_id")
    if not player_two_id:
        abort(400)
    winner = str(request.form.get("winner"))
    if not winner or (winner!="1" and winner!="2"):
        print(winner)
        abort(400)

    # Ensure Match Exists
    res = MatchHistory.query.filter(
        db.and_(
            db.or_(
                db.and_(
        MatchHistory.player_one_id==player_one_id,
        MatchHistory.player_two_id==player_two_id
        ),
                db.and_(
        MatchHistory.player_one_id==player_two_id,
        MatchHistory.player_two_id==player_one_id
        )
            )),
            MatchHistory.winner=="0"
        ).first()

    if not res:
        return "Match Not Found"

    # TODO: Check to see if user reporting result was in match

    try:
        res.winner = winner
        res.player_one_final_elo, res.player_two_final_elo = calculate_elo_change(
            res.player_one_initial_elo,
            res.player_two_initial_elo, winner
        )
        User.query.filter_by(id=player_one_id).first().elo = res.player_one_final_elo
        User.query.filter_by(id=player_two_id).first().elo = res.player_two_final_elo
        db.session.commit()
        return jsonify(
            winner=res.winner,
            match_id=res.match_id,
            p1_username=User.query.get(player_one_id).username,
            p1_old_elo=res.player_one_initial_elo,
            p1_updated_elo=res.player_one_final_elo,
            p2_username=User.query.get(player_two_id).username,
            p2_old_elo=res.player_two_initial_elo,
            p2_updated_elo=res.player_two_final_elo,
        )
    except Exception:
        abort(500)

@rps_routes.route("/match/me", methods=["GET"])
@login_required
def my_last_match():
    '''Get Last Match Route'''
    res = get_matches_from_username(session['username'])
    if not res:
        return jsonify({'error': 'No Matches Played'}), 404
    ongoing = "True" if res.winner == "0" else "False"
    return jsonify({
        "ongoing": ongoing,
        'match_id': res.match_id,
        'player_one_id': res.player_one_id,
        'player_two_id': res.player_two_id,
        'player_one_initial_elo': res.player_one_initial_elo,
        'player_two_initial_elo': res.player_two_initial_elo,
        'player_one_final_elo': res.player_one_final_elo,
        'player_two_final_elo': res.player_two_final_elo,
        'winner': res.winner,
        'player_one_ack': res.player_one_ack,
        'player_two_ack': res.player_two_ack,
        'match_created': res.match_created.strftime('%Y-%m-%d %H:%M:%S')
    })

@rps_routes.route("/match/stats", methods=["GET"])
@login_required
def my_match_stats():
    '''Get Match Stats'''
    res = get_matches_from_username(session['username'])
    if not res:
        return jsonify({'error': 'No Matches Played'}), 404
    return jsonify(get_recent_match_data(session['username']))

@rps_routes.route("/match/<match_id>", methods=["GET"])
@login_required
def fetch_match(match_id):
    '''Fetch Match Route'''
    res = MatchHistory.query.get(match_id)
    if not res:
        return jsonify({'error': 'Matches Not Found'}), 404
    ongoing = "True" if res.winner == "-1" else "False"
    return jsonify({
        "ongoing": ongoing,
        'match_id': res.match_id,
        'player_one_id': res.player_one_id,
        'player_two_id': res.player_two_id,
        'player_one_initial_elo': res.player_one_initial_elo,
        'player_two_initial_elo': res.player_two_initial_elo,
        'player_one_final_elo': res.player_one_final_elo,
        'player_two_final_elo': res.player_two_final_elo,
        'winner': res.winner,
        'player_one_ack': res.player_one_ack,
        'player_two_ack': res.player_two_ack,
        'match_created': res.match_created.strftime('%Y-%m-%d %H:%M:%S')
    })

@rps_routes.route("/report", methods=["POST"])
@login_required
def enqueue_choice():
    '''Enqueues Result for Async Implementation'''
    # they must be logged in so they must have a username
    # ensure they have user record
    res = get_user_from_username(session['username'])
    if not res:
        abort(400)

    # check to see if they are already in queue
    users_in_queue = [x.username for x in list(g.matchmaking_queue.queue)]
    if session['username'] in users_in_queue:
        abort(429)

    # Ensure Choice is present
    user_choice = request.form.get("choice")
    if not user_choice:
        abort(400)

    user_choice = user_choice.lower()
    if user_choice not in ["rock", "paper", "scissors"]:
        abort(400)

    g.matchmaking_queue.put(PlayerChoice(session['username'], user_choice))
    return 'Success!', 200

@rps_routes.route("/queuecheck", methods=["GET"])
@login_required
def check_queue():
    '''Checks to see if user in queue'''
    # they must be logged in so they must have a username
    # ensure they have user record
    res = get_user_from_username(session['username'])
    if not res:
        abort(400)

    # check to see if they are already in queue
    users_in_queue = [x.username for x in list(g.matchmaking_queue.queue)]
    if session['username'] in users_in_queue:
        abort(429)
    return 'Success!', 200
