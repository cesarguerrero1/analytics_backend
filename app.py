'''
Cesar Guerrero
08/24/23

This file is just here to communicate with the Procfile
'''
import os
from analytics_api import create_app

app = create_app(os.getenv("ENVIRONMENT"))