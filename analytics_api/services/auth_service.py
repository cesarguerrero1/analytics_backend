'''
Cesar Guerrero
08/24/23

The Authentication Service is the middle man between the controller and the model. The model will interact with the external API
and when it returns information we need to curate it such that the controller is able to use the data without having to curate
it further

'''
import os
import sys
import httpx
from authlib.integrations.httpx_client import AsyncOAuth1Client
from flask import session

#This method is used to obtain the request tokens from Twitter in preperation for a user to sign in to our site via twitter
async def obtain_twitter_request_token():
    endpoint_url = 'https://api.twitter.com/oauth/request_token'

    try:
        client = AsyncOAuth1Client(client_id=os.getenv("API_KEY"), client_secret=os.getenv("API_SECRET"), redirect_uri=os.getenv("CALLBACK_URI"))
        response = await client.fetch_request_token(endpoint_url)
        print(response.get('oauth_callback_confirmed'))
        sys.stdout.flush()
        
        #Need to verify that Twitter will know where to redirect
        if response.get('oauth_callback_confirmed') != 'true':
            print("Here")
            sys.stdout.flush()
            return False
        
        #Store our request tokens in the session
        session['oauth_token'] = response.get('oauth_token')
        session['oauth_token_secret'] = response.get('oauth_token_secret')
        return True
    
    except:
        #We failed the first-leg of OAuth1.0
        print("Never Worked...")
        sys.stdout.flush()
        return False

#This method completes the last leg of the identification process
async def obtain_twitter_access_token(oauth_verifier, session_token, session_secret):
    endpoint_url = 'https://api.twitter.com/oauth/access_token'

    try:
        client = AsyncOAuth1Client(client_id=os.getenv("API_KEY"), client_secret=os.getenv("API_SECRET"))
        response = await client.fetch_access_token(endpoint_url, verifier=oauth_verifier, token=session_token, token_secret=session_secret)
        #Store these now verified keys in the session for future API calls
        session['auth_key'] = response.get('oauth_token')
        session['auth_secret'] = response.get('oauth_token_secret')
        session['username'] = response.get('screen_name')
        session['user_id'] = response.get('user_id')
        return True
    except:
        return False