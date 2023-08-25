'''
Cesar Guerrero
08/24/23

The Authentication Controller is what will be handling all of the HTTP Endpoints for ensuring a user is
authenticated with the external API

'''
from flask import (Blueprint, request, session, url_for)
from ..services import auth_service

#Creating our blueprint so we can register with the application
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
#Eventually we want to send a paramter detailing what we are trying to login to (Twitter, Pinterest, Etc.)
async def login():
    '''
    Guidelines:
    1. When you make a GET request to the login page there should be a check of whether or not you are logged in.
        a. If you are logged in then we should redirect you to the dashobard.
        b. if you are not logged in then we should stay on the page and allow you to click on the button to login
    2. When you make a POST request then we need to now begin the authorization process
    '''

    #We need to check our session and see if the user is already logged in
    logged_in = False
    try:
        logged_in = session['is_logged_in']
    except:
        pass
    
    
    if request.method == "GET":
        if logged_in == True:
            return 'TRUE'
        else:
            #This means they are not logged in so generate our tokens in preperation
            auth_service.obtain_twitter_request_token()
            return 'FALSE'
    
    if request.method == "POST":
        return "SECRURE"

