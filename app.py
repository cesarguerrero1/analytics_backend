from flask import Flask

app = Flask(__name__)

@app.route('/')
def heroku_connection():
    return "<h1>The backend is now live on Heroku!</h1>"

