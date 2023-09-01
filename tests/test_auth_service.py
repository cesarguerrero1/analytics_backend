'''
Cesar Guerrero
08/31/23

Testing our Authorization Service file
'''

import pytest
import responses
from unittest.mock import AsyncMock, patch
from analytics_api.services import auth_service


#Mock testing our call to the Twitter API for first leg of Oauth
class TestClassRequest():
    @pytest.mark.asyncio
    @patch('analytics_api.services.auth_service.twitter_request_call', new=AsyncMock(return_value={'status':'401'}))
    async def test_obtain_twitter_request_token_fail(self):
        #Failed Request Test
        response = await auth_service.obtain_twitter_request_token()
        assert response == {'status_code': 401, 'status_message':"Unauthorized"}

    @pytest.mark.asyncio
    @patch('analytics_api.services.auth_service.twitter_request_call', new=AsyncMock(side_effect=Exception("error")))
    async def test_obtain_twitter_request_token_error(self):
        #Exception Error
        response = await auth_service.obtain_twitter_request_token()
        assert response == {'status_code': 400, 'status_message':"ERROR"}

    @pytest.mark.asyncio
    @patch('analytics_api.services.auth_service.twitter_request_call', new=AsyncMock(return_value={'status':'200', 'oauth_token':'abc', 'oauth_token_secret':'123'}))
    async def test_obtain_twitter_request_token_pass(self,client):
        #Successful Request
        with client:
            client.get('/profile')
            response = await auth_service.obtain_twitter_request_token()
            assert response == {"status_code": 200, 'oauth_token':'abc'}

#Mock testing our call to the Twitter API for the third leg of Oauth
class TestClassAuthorization():

    oauth_verifier = "aaa"
    session_token =  "bbb"
    session_secret = "ccc"

    @pytest.mark.asyncio
    @patch('analytics_api.services.auth_service.twitter_authorization_call', new=AsyncMock(return_value={'status':'401'}))
    async def test_obtain_twitter_access_token_fail(self):
        #Failed Authorization
        response = await auth_service.obtain_twitter_access_token(self.oauth_verifier, self.session_token, self.session_secret)
        assert response ==  {'status_code': 401, 'status_message':"Unauthorized"}

    @pytest.mark.asyncio
    @patch('analytics_api.services.auth_service.twitter_authorization_call', new=AsyncMock(side_effect=Exception("error")))
    async def test_obtain_twitter_access_token_error(self):
        #Exception Error
        response = await auth_service.obtain_twitter_access_token(self.oauth_verifier, self.session_token, self.session_secret)
        assert response == {'status_code': 400, 'status_message':"ERROR"}

    @pytest.mark.asyncio
    @patch('analytics_api.services.auth_service.twitter_authorization_call', new=AsyncMock(return_value={'status':'200', 'auth_key':'def', 'auth_secret':'456', 'current_user':"Me", 'user_id':'abc123'}))
    async def test_obtain_twitter_access_token_pass(self, client):
        #Succesful Authorization
        with client:
            #We need to initialize a session
            client.get('/profile')
            response = await auth_service.obtain_twitter_access_token(self.oauth_verifier, self.session_token, self.session_secret)
            assert response ==  {'status_code': 200, 'current_user':"Me"}

