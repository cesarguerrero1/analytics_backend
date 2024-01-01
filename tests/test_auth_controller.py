'''
Cesar Guerrero
08/31/23

Testing our Base Authorization Controller
'''

import pytest
from flask import session

#Testing Various Profile Route Options
class TestProfileClass:
    def test_profile_logged_in(self,client):
        #User is logged in to Twitter
        with client.session_transaction() as session:
            session["app"] = "Twitter"
            session['is_logged_in']=True
        response = client.get('/profile')
        assert response.data == b'{"app":"Twitter","is_logged_in":true,"status_code":200,"status_message":"OK"}\n'
        
        #User is logged in to Twitch
        with client.session_transaction() as session:
            session["app"] = "Twitch"
            session['is_logged_in']=True
        response = client.get('/profile')
        assert response.data == b'{"app":"Twitch","is_logged_in":true,"status_code":200,"status_message":"OK"}\n'
    
    def test_profile_not_logged_in(self,client):
        #User is not logged in
        with client.session_transaction() as session:
            session['is_logged_in']=False
        response = client.get('/profile')
        assert response.data == b'{"app":null,"is_logged_in":false,"status_code":200,"status_message":"OK"}\n'
    
    def test_profile_missing_key(self,client):
        #User is not logged in
        response = client.get('/profile')
        assert response.data == b'{"app":null,"is_logged_in":false,"status_code":200,"status_message":"OK"}\n'
    
#Testing the logout route
def test_logout(client):
    with client:
        client.get('/profile')
        assert session
        #After we call this route we get two items 
        assert session['app'] == None
        assert session['is_logged_in'] == False

        #Now we destroyed the session
        response = client.get('/logout')
        assert response.data == b'{"session_destroyed":true,"status_code":200,"status_message":"OK"}\n'

        with pytest.raises(KeyError):
            session['is_logged_in']
    
