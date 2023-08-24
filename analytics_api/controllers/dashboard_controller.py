'''
Cesar Guerrero
08/24/23

The Dashboard Controller is what will be handling all of the HTTP Endpoints once a user has been authorized.

'''

from flask import (Blueprint, request, session, url_for)
from ..services import dashboard_service

#Creating our blueprint so we can register with the application
bp = Blueprint('dashboard', __name__)

#Now we can define all of our HTTP ENDPOINTS

@bp.route('/', methods=['POST'])
@bp.route('/dashboard', methods=['POST'])
def get_analytics():
    if request.method == "POST":
        return "All analytics should appear here"