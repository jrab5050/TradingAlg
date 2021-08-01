import websocket

SOCKET = "wss://socket.polygon.io/crypto"

def on_open(ws):
    print("opened")

def on_close(ws):
    print("closed")

def on_messege(ws, messege):
    print("reciving messeges")

ws = websocket.WebSocketApp(SOCKET, on_open, on_close)
