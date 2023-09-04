'''
Cesar Guerrero
08/24/23

The Authentication Controller is what will be handling all of the HTTP Endpoints for ensuring a user is
authenticated with the external API

'''
import sys
from flask import (Blueprint, request, session, jsonify)
from ..services import auth_service

#Creating our blueprint so we can register with the application
bp = Blueprint('auth', __name__)


#Check if the user is logged in.
@bp.route('/profile', methods=['GET'])
def profile():
    return is_logged_in(session.get('is_logged_in', None))

#This route is where the one-click login call will occur
@bp.route('/login', methods=['GET'])
async def login():
    #Whenever there is a get request we want to generate tokens
    if request.method == "GET":
        
        #Call our specific service
        #NOTE: We will need to make calls to various external APIS (Twitter, Pinterest, Instagram, Etc.)
        response = await auth_service.obtain_twitter_request_token()
        #We need to alert the frontend of the status of our request
        if response['status_code'] == 200:
            response['oauth_ready'] = True
            return jsonify(response)
        else:
            response['oauth_ready'] = False
            return jsonify(response)

#This is the page that Twitter will redirect to after the user has either allowed or disallowed our app to act on their behalf
@bp.route('/callback')
async def callback():
    #Look at the request parameters
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    #The final step is to get a full-fledged credential
    if oauth_token != session['oauth_token']:
        print("Oauth token mismatch")
        sys.flush.out()
        return jsonify({'status_code': 401, 'status_message': "Unauthorized", "oauth_approved": False, "current_user": None})
    
    response = await auth_service.obtain_twitter_access_token(oauth_verifier, oauth_token, session['oauth_token_secret'])
    print("Response from service")
    print(response)
    sys.flush.out()
    #Alert the frontend to update its state
    if response['status_code'] == 200:
        session['is_logged_in'] = True
        response['oauth_approved']=True
        return jsonify(response)
    else:
        response['oauth_approved']=False
        response['current_user']=None
        print("Updated response to send to frontend")
        print(response)
        sys.flush.out()
        return jsonify(response)

#Any HTTP call to this route should immediately destroy the session
@bp.route('/logout')
def logout():
    session.clear()
    return jsonify({'status_code': 200, 'status_message': "OK", "session_destroyed": True})


############# HELPER FUNCTIONS #############

#Function to check whether a user is logged in. It will set some session key-values if no user is found
def is_logged_in(log_key):
    if log_key == True:
        #A session exists for the given user
        return jsonify({'status_code': 200, 'status_message': "OK", "is_logged_in": True, "current_user": session.get("current_user")})
    else:
        #A session does not exist for the given user
        session['is_logged_in'] = False
        session['current_user'] = None

        return jsonify({'status_code': 200, 'status_message': "OK", "is_logged_in": False, "current_user": None})