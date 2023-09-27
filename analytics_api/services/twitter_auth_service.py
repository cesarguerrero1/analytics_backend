'''
Cesar Guerrero
08/24/23

The Authentication Service is the middle man between the controller and the model. The model will interact with the external API
and when it returns information we need to curate it such that the controller is able to use the data without having to curate
it further

'''
import os
import requests #Library to make HTTP Requests
from urllib.parse import parse_qs
from flask import (session, Response, jsonify)
from requests_oauthlib import OAuth1

#This method is used to obtain the request tokens from Twitter in preperation for a user to sign in to our site via twitter
async def obtain_twitter_request_token():
    try:
        response = await twitter_request_call()
    except:
        return Response("Bad Request", status=400)
    
    if response['status_code'] != 200:
        return Response("ERROR", status=response['status_code'])

    #Store our Ouath 1st-leg Values
    session['twitter_oauth_token'] = response['oauth_token']
    session['twitter_oauth_token_secret'] = response['oauth_token_secret']

    return jsonify({"status_code": 200, 'status_message': "OK", 'oauth_ready': True, 'oauth_token': session['twitter_oauth_token']})

#This method completes the last leg of the identification process
async def obtain_twitter_access_token(oauth_verifier, session_token, session_secret):
    try:
        response = await twitter_authorization_call(oauth_verifier, session_token, session_secret)
    except:
        return Response("Bad Request", status=400)

    if response['status_code'] != 200:
        return Response("ERROR", status=response['status_code'])
    
    #Store these now verified keys in the session for future API calls
    session['twitter_auth_key'] = response['auth_key']
    session['twitter_auth_secret'] = response['auth_secret']
    session['is_logged_in'] = True
    session['app'] = "Twitter"

    return jsonify({'oauth_approved': True, "status_code": 200, 'status_message': "OK"})
    

################## Helper Function ################## 

#Call the Twitter API to get request tokens
async def twitter_request_call():
    endpoint_url = 'https://api.twitter.com/oauth/request_token'
    #Oauth Library used to help OAuth1 Flow
    oauth = OAuth1(os.getenv("TWITTER_API_KEY"), client_secret=os.getenv("TWITTER_API_SECRET"), callback_uri=os.getenv("TWITTER_CALLBACK_URI"))

    response = requests.get(url=endpoint_url, auth=oauth)

    #Respond with our new object
    response_object = {}
    response_object['status_code'] = response.status_code
    if response_object['status_code'] == 200:
        #Parse our response
        dictionary = parse_qs(response.text)
        response_object['oauth_token'] = dictionary['oauth_token'][0]
        response_object['oauth_token_secret'] = dictionary['oauth_token_secret'][0]
    return response_object

#Call the Twitter API to get full authentication tokens
async def twitter_authorization_call(oauth_verifier, session_token, session_secret):
    endpoint_url = 'https://api.twitter.com/oauth/access_token'
    
    oauth = OAuth1(os.getenv("TWITTER_API_KEY"), client_secret=os.getenv("TWITTER_API_SECRET"),
                   resource_owner_key=session_token, resource_owner_secret=session_secret,
                   verifier=oauth_verifier
            )
    
    response = requests.post(url=endpoint_url, auth=oauth)
    
    #Respond with our new object
    response_object = {}
    response_object['status_code'] = response.status_code
    if response_object['status_code'] == 200:
        #Parse our response
        dictionary = parse_qs(response.text)
        response_object['auth_key'] = dictionary['oauth_token'][0]
        response_object['auth_secret'] = dictionary['oauth_token_secret'][0]

    return response_object
