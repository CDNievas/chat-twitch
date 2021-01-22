
from flask import Flask, request
from flask_socketio import SocketIO

import Twitch

app = Flask(__name__)
sio = SocketIO(app, always_connect=True)
Twitch.setSOClient(sio)

@sio.on("info")
def response(data):
    Twitch.sendMessage(data)

@sio.on('response')
def response(data):
    Twitch.sendMessage(data)

@sio.on("handshake")
def handshake(data):
    if(data == "tinder"):
        Twitch.setTinderClient(request.sid)
    elif (data == "leds"):
        Twitch.setLedsClient(request.sid)
    elif (data == "spotify"):
        Twitch.setSpotifyClient(request.sid)
    else:
        print("Handshake incorrecto con cliente")


@sio.on("connect")
def connect():
    sio.emit("handshake","")

@sio.on("disconnect")
def disconnect():
    print("Se desconecto un cliente")

def startWebServer():
    sio.run(app, port=5000)