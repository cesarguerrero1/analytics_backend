'''
Cesar Guerrero
08/31/23

Testing our Authorization Controller
'''

import pytest
from flask import session
from unittest.mock import AsyncMock, patch

#Testing Various Profile Route Options
class TestProfileClass:
    def test_profile_logged_in(self,client):
        #User is logged in
        with client.session_transaction() as session:
            session['is_logged_in']=True
            session['current_user']='me'
        response = client.get('/profile')
        assert response.data == b'{"current_user":"me","is_logged_in":true}\n'

    def test_profile_not_logged_in(self,client):
        #User is not logged in
        with client.session_transaction() as session:
            session['is_logged_in']=False
        response = client.get('/profile')
        assert response.data == b'{"current_user":null,"is_logged_in":false}\n'
    
    def test_profile_missing_key(self,client):
        #User is not logged in
        response = client.get('/profile')
        assert response.data == b'{"current_user":null,"is_logged_in":false}\n'
    
#Testing the login Route
class TestLoginClass:

    @patch('analytics_api.services.auth_service.obtain_twitter_request_token', new=AsyncMock(return_value={"status_code": 200, "oauth_token": "abc"}))
    def test_login_good_response(self,client):
        #You should not be able to call login with anything other than GET
        assert client.post('/login').status_code == 405
        assert client.get('/login').status_code == 200
        response = client.get('/login')
        assert response.data == b'{"oauth_ready":true,"oauth_token":"abc","status_code":200}\n'

    @patch('analytics_api.services.auth_service.obtain_twitter_request_token', new=AsyncMock(return_value={"status_code": 401, "status_message": "Unauthorized"}))
    def test_login_bad_response(self,client):
        response = client.get('/login')
        assert response.data == b'{"oauth_ready":false}\n'

#Testing the Callback Route
class TestCallbackClass:
    
    @patch('analytics_api.services.auth_service.obtain_twitter_access_token', new=AsyncMock(return_value={"status_code": 200, "current_user": 'me'}))
    def test_callback_good_response(self,client):
        with client.session_transaction() as session:
            session['oauth_token'] = "abc123" #Setting up a session variable
            session['oauth_token_secret'] = '?'
        response = client.get('/callback?oauth_token=%s&oauth_verifier=%s' %("abc123", "789xyz"))
        assert response.data == b'{"current_user":"me","oauth_approved":true,"status_code":200}\n'

    @patch('analytics_api.services.auth_service.obtain_twitter_access_token', new=AsyncMock(return_value={"status_code": 401, "status_message": "Unauthorized"}))
    def test_callback_bad_response(self,client):
        with client.session_transaction() as session:
            #Setting up session variables
            session['oauth_token'] = "abc123" 
            session['oauth_token_secret'] = '?'
        response = client.get('/callback?oauth_token=%s&oauth_verifier=%s' %("abc123", "789xyz"))
        assert response.data == b'{"current_user":null,"oauth_approved":false}\n'

    @patch('analytics_api.services.auth_service.obtain_twitter_access_token', new=AsyncMock(return_value={"status_code": 200, "current_user": 'me'}))
    def test_callback_token_mismatch(self,client):
        with client.session_transaction() as session:
            #Setting up session variables
            session['oauth_token'] = "abc123"
            session['oauth_token_secret'] = '?'
        response = client.get('/callback?oauth_token=%s&oauth_verifier=%s' %("abc124", "789xyz"))
        assert response.data == b'{"current_user":null,"oauth_approved":false}\n' #Mismatch of tokens even though we have a good response


#Testing the logout route
def test_logout(client):
    with client:
        client.get('/profile')
        assert session
        #After we call this route we get two items 
        assert session['is_logged_in'] == False
        assert session['current_user'] == None
        client.get('/logout')
        with pytest.raises(KeyError):
            session['is_logged_in']
    
