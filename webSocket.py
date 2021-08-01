import time
import ast
import json
import pprint
import sqlite3
import pandas as pd

from typing import List
from polygon import WebSocketClient, CRYPTO_CLUSTER


def my_custom_process_message(message):
    print("Recivin messages")
    json_message = json.loads(message)
    pprint.pprint(json_message)

    def add_message_to_list(message):
        messages.append(ast.literal_eval(message))

    return add_message_to_list


def my_custom_error_handler(ws, error):
    print("Error", error)


def my_custom_close_handler(ws):
    print("Closing")


def main():
    key = 'IR69iir3RqApPUaedAHTSJ2UuTJ9ASlB'
    messages = []
    my_client = WebSocketClient(CRYPTO_CLUSTER, key, my_custom_process_message)
    my_client.run_async()


    a = my_client.subscribe("XL2.DOGE-USD")
    #time.sleep(1)

    #my_client.close_connection()

    df = pd.DataFrame(messages)

if __name__ == "__main__":
    main()
