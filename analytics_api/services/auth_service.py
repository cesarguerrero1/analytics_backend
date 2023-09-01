'''
Cesar Guerrero
08/24/23

The Authentication Service is the middle man between the controller and the model. The model will interact with the external API
and when it returns information we need to curate it such that the controller is able to use the data without having to curate
it further

'''
import os
import oauth2 as oauth
import urllib
from flask import session

#This method is used to obtain the request tokens from Twitter in preperation for a user to sign in to our site via twitter
async def obtain_twitter_request_token():
    try:
        #Oauth2 Library Calls 
        response = await twitter_request_call()
    except:
        return {"status_code": 400, "status_message": "ERROR"}
    
    if response['status'] != '200':
        return {"status_code": int(response['status']), "status_message": "Unauthorized"}
    
    #Store our Ouath 1st-leg Values
    session['oauth_token'] = response['oauth_token']
    session['oauth_token_secret'] = response['oauth_token_secret']

    return {"status_code": 200, 'oauth_token': session['oauth_token']}

#This method completes the last leg of the identification process
async def obtain_twitter_access_token(oauth_verifier, session_token, session_secret):
    try:
        response = await twitter_authorization_call(oauth_verifier, session_token, session_secret)
    except:
        return {"status_code": 400, "status_message": "ERROR"}

    if response['status'] != '200':
        return {"status_code": int(response['status']), "status_message": "Unauthorized"}
    
    #Store these now verified keys in the session for future API calls
    session['auth_key'] = response['auth_key']
    session['auth_secret'] = response['auth_secret']
    session['current_user'] = response['current_user']
    session['user_id'] = response['user_id']

    return {"status_code": 200, "current_user": session['current_user']}
    

##### HELPER FUNCTIONS ######

#Call the Twitter API to get request tokens
async def twitter_request_call():
    endpoint_url = 'https://api.twitter.com/oauth/request_token'
    consumer = oauth.Consumer(os.getenv("API_KEY"), os.getenv("API_SECRET"))
    client = oauth.Client(consumer)
    client_response,content = client.request(endpoint_url, "POST", body=urllib.parse.urlencode({"oauth_callback": os.getenv("CALLBACK_URI")}))
    print(client_response,content)
    #Build our response object
    response = {}
    response['status'] = client_response['status']

    if response['status'] == '200':
        request_token = dict(urllib.parse.parse_qsl(content))
        response['oauth_token'] = request_token[b'oauth_token'].decode('utf-8')
        response['oauth_token_secret'] = request_token[b'oauth_token_secret'].decode('utf-8')

    return response


#Call the Twitter API to get full authentication tokens
async def twitter_authorization_call(oauth_verifier, session_token, session_secret):
    endpoint_url = 'https://api.twitter.com/oauth/access_token'

    #Create our oauth call
    consumer = oauth.Consumer(os.getenv("API_KEY"), os.getenv("API_SECRET"))
    token = oauth.Token(session_token, session_secret)
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    client_response, content = await client.request(endpoint_url, "POST")

    #Build our response object
    response = {}
    response['status'] = client_response['status']
    
    if response['status'] == '200':
        access_token = dict(urllib.parse.parse_qsl(content))
        response['auth_key'] = access_token[b'oauth_token'].decode('utf-8')
        response['auth_secret'] = access_token[b'oauth_token_secret'].decode('utf-8')
        response['current_user'] = access_token[b'screen_name'].decode('utf-8')
        response['user_id'] = access_token[b'user_id'].decode('utf-8')
    
    return response

