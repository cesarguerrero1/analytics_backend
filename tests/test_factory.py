'''

Cesar Guerrero
08/31/23

Testing our factory creation

'''

from analytics_api import create_app

#Testing different configurations
def test_config(monkeypatch):
    #Monkeypatch is used to simulate our enivornmental variables storage
    monkeypatch.setenv("SECRET_KEY",'abc')

    #Production Build
    prod_app = create_app("PRODUCTION") 
    assert prod_app.secret_key == 'abc'
    assert prod_app.config['SESSION_COOKIE_HTTPONLY'] == True
    assert not prod_app.testing
       
    #Development Build
    dev_app = create_app("DEV") 
    assert dev_app.secret_key == 'dev'
    assert dev_app.config['SESSION_COOKIE_HTTPONLY'] == False
    assert not dev_app.testing

    #Testing Build
    test_app = create_app("TESTING")
    assert test_app.secret_key =='test'
    assert test_app.testing