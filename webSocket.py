import time
import ast
import json
import pprint
import sqlite3
import pandas as pd

from typing import List
from polygon import WebSocketClient, CRYPTO_CLUSTER

frames = []


def my_custom_process_message(message):
    print("Recivin messages")
    json_message = json.loads(message)
    df = pd.DataFrame(json_message)
    frames.append(df)
    #df.to_excel("tble.xlsx", sheet_name="Sheet1")
    #print(type(json_message))
    print(df.head)

    
    
#    pprint.pprint(json_message)

    def add_message_to_list(message):
        messages.append(ast.literal_eval(message))

    return add_message_to_list


def my_custom_error_handler(ws, error):
    print("Error", error)


def my_custom_close_handler(ws):
    print("Closing")



def main():
    key = 'IR69iir3RqApPUaedAHTSJ2UuTJ9ASlB'
    my_client = WebSocketClient(CRYPTO_CLUSTER, key, my_custom_process_message)
    my_client.run_async()


    a = my_client.subscribe("XL2.DOGE-USD")
    time.sleep(5)

    my_client.close_connection()

#    frames[3].to_excel("tble.xlsx",sheet_name='TheSheet')
    final = pd.concat(frames[slice(3, len(frames))])
    final.to_excel('tble.xlsx', sheet_name='TheSheet')

#    framNum = 3
#    sheetNum = 1
#    for frame in frames:
#        sheet_name = f"Sheet{sheetNum}"
#        frame[framNum].to_excel(f"tble{sheetNum}.xlsx", sheet_name=sheet_name)
#        sheetNum += 1
#        framNum += 1



if __name__ == "__main__":
    main()
