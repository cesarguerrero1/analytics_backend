'''
Cesar Guerrero
08/31/23

Testing our Authorization Controller
'''

import pytest
import responses
from flask import session
from analytics_api.controllers.auth_controller import is_logged_in


#MOCKING OUR ENVIRONMENTAL VARIABLES
@pytest.fixture
def mock_env_is_logged_in_true(monkeypatch):
    monkeypatch.setenv("is_logged_in", True)

@pytest.fixture
def mock_env_is_logged_in_false(monkeypatch):
    monkeypatch.setenv("is_logged_in", False)


#Testing Various Profile Route Options
class TestClass:
    pass

#Testing the login route
def test_login():
    pass

#Testing the callback route
def test_callback():
    pass


#Testing the logout route
def test_logout(client):
    #Only GET methods are allowed at logout
    assert client.get('/logout').status_code == 200
    assert client.post('/logout').status_code == 405 #405 Error == Method Not Allowed

    response = client.get('/logout')
    assert response.data == b'{"session_destroyed":true}\n'
    assert not session
