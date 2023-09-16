from flask import Flask
from flask_session import Session
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#from flask_socketio import SocketIO
#import websockets
#socketio = SocketIO(app)

from routes import *

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run(port=8085, host='0.0.0.0', debug=True))
