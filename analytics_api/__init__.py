'''
Cesar Guerrero
08/24/23

This file serves as our 'Application Factory'. Depending on the environment, we should be doing different things!
'''

import os
from flask import Flask
from .controllers import (auth_controller, dashboard_controller)

def create_app():
    app = Flask(__name__)

    if os.getenv("ENVIRONMENT") == "PRODUCTION":
        print("Production")
    else:
        print("Development")
    
    #Register all of our controllers
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(dashboard_controller.bp)

    return app