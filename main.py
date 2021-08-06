import websocket
from polygon import WebSocketClient, CRYPTO_CLUSTER

SOCKET = "wss://socket.polygon.io/crypto"
key = 'IR69iir3RqApPUaedAHTSJ2UuTJ9ASlB'

def on_open(ws):
    print("opened")

def on_close(ws):
    print("closed")

def on_messege(ws, messege):
    print("reciving messeges")

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_messege)

