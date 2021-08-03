from os import times
import time
import ast
import json
import pprint
import sqlite3
import pandas as pd

from typing import List
from pandas.core.frame import DataFrame
from pandas import ExcelWriter
from polygon import WebSocketClient, CRYPTO_CLUSTER

frames = []


def my_custom_process_message(message):
    #print("Recivin messages")
    json_message = json.loads(message)
    df = pd.DataFrame(json_message)
    frames.append(df)
    #df.to_excel("tble.xlsx", sheet_name="Sheet1")
    #print(type(json_message))
    #print(df.head)

    
    
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
    my_dict = {}
    timeStamp = 0
    askPrice = 0
    askVol = 0
    Times = []
    Prices = []
    Volumes = []
    ew = pd.ExcelWriter('tble2.xlsx', engine='xlsxwriter', mode='w')


    a = my_client.subscribe("XL2.DOGE-USD")
    time.sleep(2)

    my_client.close_connection()

    #print(frames[3:len(frames)])
    count = 1
    my_dict = {'Time': [], 'Price': [], 'Volume': []}
    for frame in frames[3:len(frames)]:


        if (frame['x'][0]) == 1:
            my_dict['Time'].append(frame['t'][0])
            print(timeStamp)

            #print((frame))
            my_dict['Price'].append(frame['a'][0][0][0])
            print('askPrice: ', askPrice)
            
            my_dict['Volume'].append(frame['a'][0][0][1])
            print('askVol: ', askVol)

        
    sheet_name = f'Sheet{count}'
    pd.DataFrame(my_dict).to_excel(ew, sheet_name=sheet_name)
            

    print(my_dict)



    ew.save()




    print('------------------------printed asks------------------------')


if __name__ == "__main__":
    main()
