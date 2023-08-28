'''
Cesar Guerrero
08/24/23

The Authentication Controller is what will be handling all of the HTTP Endpoints for ensuring a user is
authenticated with the external API

'''
import sys
from flask import (Blueprint, request, session, jsonify, url_for)
from ..services import auth_service

#Creating our blueprint so we can register with the application
bp = Blueprint('auth', __name__)


#Check if the user is logged in.
@bp.route('/profile', methods=['GET'])
def profile():
    if session.get('is_logged_in', None) != None:
        #A session exists for the given user
        return jsonify({"is_logged_in": True, "current_user": session.get("username")})
    else:
        #A session does not exist for the given user
        return jsonify({"is_logged_in": False, "current_user": None})

#This route is where the one-click login will occur -- Eventually we want to send a paramter detailing what we are trying to login to (Twitter, Pinterest, Etc.)
@bp.route('/login', methods=['GET'])
async def login():
    '''
    Guidelines:
    1. When you make a GET request to the login page there should be a check of whether or not you are logged in.
        a. If you are logged in then we should redirect you to the dashboard.
        b. if you are not logged in then we should stay on the page and allow you to click on the button to login
    2. When you make a POST request then we need to now begin the authorization process
    '''
    if request.method == "GET":
        #This means they are not logged in so generate our tokens in preperation
        response = await auth_service.obtain_twitter_request_token()

        #We need to alert the frontend of the status of our request
        if response:
            return jsonify({"oauth_ready": True, "oauth_token": session.get("oauth_token")})
        else:
            return jsonify({"oauth_ready": False})

#This is the page that Twitter will redirect to after the user has either allowed or disallowed our app to act on their behalf
@bp.route('/callback')
async def callback():
    print(session)
    sys.stdout.flush()
    #Look at the request parameters
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    #The final step is to get a full-fledged credential
    if oauth_token != session['oauth_token']:
        return jsonify({"oauth_approved": False, "current_user": None})
    
    response = await auth_service.obtain_twitter_access_token(oauth_verifier, oauth_token, session['oauth_token_secret'])

    if response:
        return jsonify({"oauth_approved": False, "current_user": session.get("username")})
    else:
        return jsonify({"oauth_approved": False, "current_user": None})

#Any HTTP call to this route should immediately destroy the session
@bp.route('/logout')
def logout():
    session.clear()
    return 'TRUE'
