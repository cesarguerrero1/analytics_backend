'''
Cesar Guerrero
09/19/23

The Authentication Service is the middle man between the controller and the model. The model will interact with the external API
and when it returns information we need to curate it such that the controller is able to use the data without having to curate
it further

'''
import os
import requests
from urllib.parse import urlencode
from flask import (session, json, Response, jsonify)

#This method is used to authorize our Twitch Access Token
async def obtain_twitch_access_token(code):
    try:
       response = await twitch_authorization_call(code)
    except:
        return Response("Bad Request", status=400)
    
    if response['status_code'] != 200:
        return Response("ERROR", status=response['status_code'])
    
    #Update our session
    session['twitch_access_token'] = response['access_token']
    session['twitch_refresh_token'] = response['refresh_token']
    session['is_logged_in'] = True
    session['app'] = "Twitch"

    return jsonify({"oauth_approved": True, "status_code": 200, "status_message": "OK"})


################## Helper Function ##################

#This method is a helper function directly calling the Twitch API
async def twitch_authorization_call(code):
    endpoint_url = 'https://id.twitch.tv/oauth2/token'
    
    body = {
        "client_id": os.getenv("TWITCH_API_KEY"),
        "client_secret": os.getenv("TWITCH_API_SECRET"),
        "code":code,
        "grant_type":"authorization_code",
        "redirect_uri": os.getenv("TWITCH_CALLBACK_URI")
    }

    response = requests.post(url=endpoint_url, data=urlencode(body))
    
    #Respond with our new object
    response_object = {}
    response_object['status_code'] = response.status_code
    if response_object['status_code'] == 200:
        #Parse our response
        dictionary = json.loads(response.text)
        response_object['access_token'] = dictionary['access_token']
        response_object['refresh_token'] = dictionary['refresh_token']

    return response_object
