'''
Cesar Guerrero
08/31/23

This is to setup your test environment in PyTest
'''

import pytest
from analytics_api import create_app

#We are creating an instance of our app for our tests to use
@pytest.fixture()
def app():
    app = create_app("TESTING") #The default is None
    yield app

#Our test will call client so that they can make requests to the server without it being on
@pytest.fixture()
def client(app):
    return app.test_client()