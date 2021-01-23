
from flask import Flask, request
from flask_socketio import SocketIO
import os
import Twitch

from dotenv import load_dotenv

load_dotenv()

PORT_WS = int(os.getenv("PORT_WS"))

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
        print("Se conecto TinderTwitch")
    elif (data == "leds"):
        Twitch.setLedsClient(request.sid)
        print("Se conecto LedsTwitch")
    elif (data == "spotify"):
        Twitch.setSpotifyClient(request.sid)
        print("Se conecto SpotifyTwitch")
    else:
        print("Handshake incorrecto con cliente")


@sio.on("connect")
def connect():
    sio.emit("handshake","")

@sio.on("disconnect")
def disconnect():
    print("Se desconecto un cliente")

def startWebServer():
    sio.run(app, port=PORT_WS)
