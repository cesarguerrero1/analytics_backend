'''
Cesar Guerrero
09/17/23

This controller will handle any authentication needs with Twitch

'''

import os
from flask import (Blueprint, request, Response, jsonify)
from ..services import twitch_auth_service

#Creating our blueprint so we can register with the application
bp = Blueprint('twitch_auth', __name__)

#We are returning the 'Client-Id' so that we can begin the Oauth2 flow for Twitch 
@bp.route('/login/twitch', methods=['GET'])
async def twitch_login():
    if request.method == "GET":
        return jsonify({"client_id": os.getenv("TWITCH_API_KEY"), "oauth_ready": True, "status_code":200, "status_message":"OK"})

#This is URL that will be pinged after the user has allowed our application to act on their behalf
@bp.route('/callback/twitch')
async def twitch_callback():
    #Look at the request parameters
    code = request.args.get('code')

    #Dont bother pinging Twitch if we don't have a code
    if code == None:
        return Response("Unauthorized", status=401)

    response = await twitch_auth_service.obtain_twitch_access_token(code)
    
    return response


