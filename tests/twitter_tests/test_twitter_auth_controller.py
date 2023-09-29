'''
Cesar Guerrero
09/27/23

Testing our Twitter Authorization Controller
'''

import pytest
from flask import session
from unittest.mock import AsyncMock, patch

#Testing our 'Login with Twitter' Route
class TestLoginClass:

    @patch('analytics_api.services.twitter_auth_service.obtain_twitter_request_token', new=AsyncMock(return_value={"status_code": 200, "status_message":"OK", "oauth_ready": True, "oauth_token": "abc"}))
    def test_login_response(self,client):
        #You should not be able to call login with anything other than GET
        assert client.post('/login/twitter').status_code == 405
        assert client.get('/login/twitter').status_code == 200
        #Testing that we correctly receiving a response from our function call
        response = client.get('/login/twitter')
        assert response.data == b'{"oauth_ready":true,"oauth_token":"abc","status_code":200,"status_message":"OK"}\n'


#Testing our Callback for the Twitter Oauth Flow
class TestCallbackClass:

    #Notice we don't need to mock our service function as it will never be called
    def test_invalid_oauth_token_callback(self, client):
        with client.session_transaction() as session:
            #Setting up session variables
            session['twitter_oauth_token'] = "abc123" 
        #OAuth Token Mismatch
        response = client.get('/callback/twitter?oauth_token=%s&oauth_verifier=%s' %("456def", "789xyz"))
        assert response.data == b'Unauthorized'
        assert response.status_code == 401

    @patch('analytics_api.services.twitter_auth_service.obtain_twitter_access_token', new=AsyncMock(return_value={'oauth_approved': True, "status_code": 200, 'status_message': "OK"}))
    def test_callback_response(self, client):
        with client.session_transaction() as session:
            #Setting up session variables
            session['twitter_oauth_token'] = "abc123" 
            session['twitter_oauth_token_secret'] = "456def"
        response = client.get('/callback/twitter?oauth_token=%s&oauth_verifier=%s' %("abc123", "789xyz"))
        assert response.data == b'{"oauth_approved":true,"status_code":200,"status_message":"OK"}\n'