from threading import Thread
from WS import startWebServer
from Twitch import startTwitchChat


def main():
    threadWS = Thread(target = startWebServer)
    threadTwitch = Thread(target=startTwitchChat)
    threadWS.start()
    threadTwitch.start()
    
main()
