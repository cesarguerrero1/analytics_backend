'''
Cesar Guerrero
08/24/23

The Twitter Authentication Service is the middle man between the controller and the model. The model will interact with the external API
and when it returns information we need to curate it such that the controller is able to use the data without having to curate
it further

'''
import os
import requests #Library to make HTTP Requests
from urllib.parse import parse_qs
from flask import (session, Response, jsonify, current_app)
from requests_oauthlib import OAuth1

#This method is used to obtain the request tokens from Twitter in preperation for a user to sign in to our site via twitter
async def obtain_twitter_request_token():
    try:
        response = await twitter_request_call()

        return response
    
    except:
        return Response("Bad Request", status=400)


#This method completes the last leg of the identification process
async def obtain_twitter_access_token(oauth_verifier, session_token, session_secret):
    try:
        response = await twitter_authorization_call(oauth_verifier, session_token, session_secret)

        return response

    except:
        return Response("Bad Request", status=400) 

################## Helper Function ################## 

#Call the Twitter API to get request tokens
async def twitter_request_call():
    endpoint_url = 'https://api.twitter.com/oauth/request_token'
    
    #Recall that we are doing this check for test mode so we can remove the need to call/mock OAuth1
    if current_app.config['TESTING'] == True:
        response = requests.get(url=endpoint_url)
    else:
        #Oauth Library used to help OAuth1 Flow
        oauth = OAuth1(os.getenv("TWITTER_API_KEY"), client_secret=os.getenv("TWITTER_API_SECRET"), callback_uri=os.getenv("TWITTER_CALLBACK_URI"))

        response = requests.get(url=endpoint_url, auth=oauth)

    response_object = {}
    #Respond with our new object
    if response.status_code == 200:
        response_object['status_code'] = 200
        response_object['status_message'] = "OK"
        response_object['oauth_ready'] = True
        dictionary = parse_qs(response.text)
        response_object['oauth_token'] = dictionary['oauth_token'][0]

        #Store our Ouath 1st-leg Values
        session['twitter_oauth_token'] = dictionary['oauth_token'][0]
        session['twitter_oauth_token_secret'] = dictionary['oauth_token_secret'][0]

        return jsonify(response_object)

    else:
        return Response("ERROR", status=response.status_code)

#Call the Twitter API to get full authentication tokens
async def twitter_authorization_call(oauth_verifier, session_token, session_secret):
    endpoint_url = 'https://api.twitter.com/oauth/access_token'
    
    if current_app.config['TESTING'] == True:
       response = requests.post(url=endpoint_url)

    else:
        oauth = OAuth1(os.getenv("TWITTER_API_KEY"), client_secret=os.getenv("TWITTER_API_SECRET"),
                    resource_owner_key=session_token, resource_owner_secret=session_secret,
                    verifier=oauth_verifier
                )
        
        response = requests.post(url=endpoint_url, auth=oauth)

    response_object = {}
    if response.status_code == 200:
        response_object["status_code"] = 200
        response_object["status_message"] = "OK"
        response_object["oauth_approved"] = True

        #Parse our response and store items 
        dictionary = parse_qs(response.text)
        session['twitter_auth_key'] = dictionary['oauth_token'][0]
        session['twitter_auth_secret'] = dictionary['oauth_token_secret'][0]
        session['is_logged_in'] = True
        session['app'] = "Twitter"

        return jsonify(response_object)

    else:
        return Response("ERROR", status=response.status_code)