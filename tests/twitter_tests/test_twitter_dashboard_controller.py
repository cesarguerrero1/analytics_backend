'''
Cesar Guerrero
09/27/23

Testing the Twitter Dashboard Controller

'''

import pytest
from flask import session
from unittest.mock import AsyncMock, patch

class TestUserPayload:
    
    @patch('analytics_api.services.twitter_dashboard_service.getTwitterUserData', new=AsyncMock(return_value={"created_at":"some-date-here", "followers_count":5, "following_count":10, "profile_image_url":"url-goes-here", "status_code":200, "status_message":"OK", "tweet_count":30, "username":"twitter-username"}))
    def test_user_payload_retrieval(self,client):
        #We need access to our session
        with client.session_transaction() as session:
            #Setting up session variables
            session['twitter_auth_key'] = "abc123" 
            session['twitter_auth_secret'] = "456def"
        response = client.get('/dashboard/twitter/users')
        assert response.status_code == 200
        assert response.data == b'{"created_at":"some-date-here","followers_count":5,"following_count":10,"profile_image_url":"url-goes-here","status_code":200,"status_message":"OK","tweet_count":30,"username":"twitter-username"}\n'

class TestTweetPayload:
   
    def test_tweet_payload_retreival(self, client):
        response = client.get('/dashboard/twitter/tweets')
        assert response.status_code == 200
        assert response.data == b'No Data'
       