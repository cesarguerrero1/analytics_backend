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

#Now we can define all of our HTTP ENDPOINTS

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return "Unsecure"
    elif request.method == "POST":
        return auth_service.login()
