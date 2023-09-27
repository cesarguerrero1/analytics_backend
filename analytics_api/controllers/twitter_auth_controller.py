'''
Cesar Guerrero
09/17/23

This controller will handle any authentication needs with Twitter

'''

from flask import (Blueprint, request, session, Response)
from ..services import twitter_auth_service

#Creating our blueprint so we can register with the application
bp = Blueprint('twitter_auth', __name__)

#This route is where the one-click login call will occur
@bp.route('/login/twitter', methods=['GET'])
async def twitter_login():
    #Whenever there is a get request we want to generate tokens
    if request.method == "GET":
        #Call our specific service
        response = await twitter_auth_service.obtain_twitter_request_token()

        #We need to alert the frontend of the status of our request
        return response

#This is the page that Twitter will redirect to after the user has either allowed or disallowed our app to act on their behalf
@bp.route('/callback/twitter')
async def twitter_callback():
    #Look at the request parameters
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    
    #The final step is to get a full-fledged credential
    if oauth_token != session['twitter_oauth_token']:
        return Response("Unauthorized", status=401)
    
    response = await twitter_auth_service.obtain_twitter_access_token(oauth_verifier, oauth_token, session['twitter_oauth_token_secret'])
    return response
