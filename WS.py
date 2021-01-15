
from flask import Flask, request
from flask_socketio import SocketIO

import Twitch

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, always_connect=True)
Twitch.setSOClient(sio)

@sio.on('response')
def response(data):
    Twitch.sendMessage(data)

@sio.on("handshake")
def handshake(data):
    if(data == "tinder"):
        Twitch.setTinderClient(request.sid)
    elif (data == "leds"):
        Twitch.setLedsClient(request.sid)
    else:
        print("Error")

@sio.on("connect")
def connect():
    sio.emit("handshake","")

@sio.on("disconnect")
def disconnect():
    sio.emit("handshake","")

def startWebServer():
    sio.run(app, port=5000)