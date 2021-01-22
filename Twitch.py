import socket, re, os, sys
from dotenv import load_dotenv

load_dotenv()

TWITCH_SERVER = os.getenv("TWITCH_SERVER")
TWITCH_PORT = int(os.getenv("TWITCH_PORT"))
TWITCH_AUTH = os.getenv("TWITCH_AUTH")
TWITCH_CHANNEL = os.getenv("TWITCH_CHANNEL")
TWITCH_USERNAME = os.getenv("TWITCH_USERNAME")

s = socket.socket()
CHANNEL = None

tinderSckt = None
ledsSckt = None
spotifySckt = None
sio = None

def startTwitchChat():
    try:
        connect(TWITCH_SERVER,TWITCH_PORT,TWITCH_AUTH,TWITCH_CHANNEL,TWITCH_USERNAME)
    except BaseException as e:
        print(e)
        print("Can't connect to Twitch Server")
        sys.exit(-3)

def setSOClient(sckt):
    global sio
    sio = sckt

def setLedsClient(sckt):
    global ledsSckt
    ledsSckt = sckt

def setTinderClient(sckt):
    global tinderSckt
    tinderSckt = sckt

def setSpotifyClient(sckt):
    global spotifySckt
    spotifySckt = sckt

def sendMessage(msg):
    s.send("PRIVMSG {} :{}\r\n".format(CHANNEL, msg).encode("utf-8"))

def connect(server,port,auth,channel,username):
    global CHANNEL
    CHANNEL = channel
    
    s.connect((server, port))
    s.send("PASS {}\n".format(auth).encode('utf-8'))
    s.send("NICK {}\n".format(username).encode('utf-8'))
    s.send("JOIN {}\n".format(channel).encode('utf-8'))

    print("Conectado al chat de Twitch correctamente")

    while True:
        resp = s.recv(4096).decode('utf-8')
        msgs = [_parseMessage(line)
                for line in filter(None, resp.split('\r\n'))]
        msgs = [r for r in msgs if r]
        
        for msg in msgs:
            _parseCommand(msg)

def _parseCommand(msg):
    global tinderSckt, ledsSckt
    message = msg["message"].lower()
    user = msg["username"]

    if user == "nightbot":
        return

    if "!leds " in message:
        color = re.findall(r"!leds \.?([ \w.]+)", message, re.IGNORECASE | re.MULTILINE)
        
        if(color == []):
            color.append("")
        
        color = color[0]

        comm = {}
        comm["color"] = color
        comm["user"] = user

        sio.emit("message",comm,to=ledsSckt)
       
    elif "!tinder" in message:
        
        comm = {}
        comm["user"] = user
        sio.emit("message",comm,to=tinderSckt)

    elif "!song" in message:

        comm = {}
        comm["user"] = user
        sio.emit("actualSong",comm,to=spotifySckt)

    elif "!playlist" in message:

        comm = {}
        comm["user"] = user
        sio.emit("playlist",comm,to=spotifySckt)
    

def _parseMessage(data):

    if _check_has_ping(data):
        s.send("PONG\r\n".encode("utf-8"))
        print("Pong enviado")

    if _check_has_channel(data):
        CHANNEL = \
            _check_has_channel(data)[0]

    if _check_has_message(data):
        return {
            'channel': re.findall(r'^:.+![a-zA-Z0-9_]+'
                                    r'@[a-zA-Z0-9_]+'
                                    r'.+ '
                                    r'PRIVMSG (.*?) :',
                                    data)[0],
            'username': re.findall(r'^:([a-zA-Z0-9_]+)!', data)[0],
            'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)',
                                    data)[0]
        }

def _check_has_ping(data):
        return re.match(
            r'^PING :tmi\.twitch\.tv$', data)

def _check_has_channel(data):
    return re.findall(
        r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+'
        r'\.tmi\.twitch\.tv '
        r'JOIN #([a-zA-Z0-9_]+)$', data)

def _check_has_message(data):
    return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+'
                    r'\.tmi\.twitch\.tv '
                    r'PRIVMSG #[a-zA-Z0-9_]+ :.+$', data)