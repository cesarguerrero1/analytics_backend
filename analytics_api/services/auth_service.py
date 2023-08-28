'''
Cesar Guerrero
08/24/23

The Authentication Service is the middle man between the controller and the model. The model will interact with the external API
and when it returns information we need to curate it such that the controller is able to use the data without having to curate
it further

'''
import os
import sys
import oauth2 as oauth
import urllib
import httpx
from flask import session

#This method is used to obtain the request tokens from Twitter in preperation for a user to sign in to our site via twitter
async def obtain_twitter_request_token():
    endpoint_url = 'https://api.twitter.com/oauth/request_token'
    print(os.getenv("API_KEY"))
    print(os.getenv("API_SECRET"))
    print(os.getenv("CALLBACK_URI"))
    sys.stdout.flush()

    try:
        consumer = oauth.Consumer(os.getenv("API_KEY"), os.getenv("API_SECRET"))
        client = oauth.Client(consumer)
        response, content = client.request(endpoint_url, "POST", body=urllib.parse.urlencode({"oauth_callback": os.getenv("CALLBACK_URI")}))
        request_token = dict(urllib.parse.parse_qsl(content))
        print(request_token)
        sys.stdout.flush()
        
        if response['status'] != '200':
            print("Failed to get token")
            sys.stdout.flush()
            return False

        session['oauth_token'] = request_token[b'oauth_token'].decode('utf-8')
        session['oauth_token_secret'] = request_token[b'oauth_token_secret'].decode('utf-8')
        return True
    
    except Exception as e:
        #We failed the first-leg of OAuth1.0
        print(e)
        sys.stdout.flush()
        return False

#This method completes the last leg of the identification process
async def obtain_twitter_access_token(oauth_verifier, session_token, session_secret):
    endpoint_url = 'https://api.twitter.com/oauth/access_token'

    try:
        #client = AsyncOAuth1Client(client_id=os.getenv("API_KEY"), client_secret=os.getenv("API_SECRET"))
        #response = await client.fetch_access_token(endpoint_url, verifier=oauth_verifier, token=session_token, token_secret=session_secret)
        #Store these now verified keys in the session for future API calls
        #session['auth_key'] = response.get('oauth_token')
        #session['auth_secret'] = response.get('oauth_token_secret')
        #session['username'] = response.get('screen_name')
        #session['user_id'] = response.get('user_id')
        return True
    except:
        return False