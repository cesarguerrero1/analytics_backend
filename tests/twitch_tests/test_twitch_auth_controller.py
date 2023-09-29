'''
Cesar Guerrero
09/27/23

Testing our Twitch Authorization Controller
'''

import pytest
from unittest.mock import AsyncMock, patch

#Testing our 'Login with Twitch' Route
class TestTwitchLoginClass:

    def test_twitch_login_response(self,client, monkeypatch):
        monkeypatch.setenv("TWITCH_API_KEY",'abc')

        #You should not be able to call login with anything other than GET
        assert client.post('/login/twitch').status_code == 405
        assert client.get('/login/twitch').status_code == 200

        #Testing that we correctly receiving a response from our function call
        response = client.get('/login/twitch')
        assert response.data == b'{"client_id":"abc","oauth_ready":true,"status_code":200,"status_message":"OK"}\n'

class TestTwitchCallbackClass:

    def test_null_code_callback(self, client):
        response = client.get('/callback/twitch')
        assert response.status_code == 401
        assert response.data == b'Unauthorized'

    @patch('analytics_api.services.twitch_auth_service.obtain_twitch_access_token', new=AsyncMock(return_value={"oauth_approved": True, "status_code": 200, "status_message": "OK"}))
    def test_twitch_callback_response(self, client):
        response = client.get('/callback/twitch?code=%s' %('abc123'))
        assert response.data == b'{"oauth_approved":true,"status_code":200,"status_message":"OK"}\n'
    