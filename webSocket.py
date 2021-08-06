from os import times
import time
import json
import pprint
import pandas as pd
import sys

from tabulate import tabulate
from pandas.core.frame import DataFrame
from pandas import ExcelWriter
from polygon import WebSocketClient, CRYPTO_CLUSTER

frames = []
data = {"Price": [], "Volume": []}


def my_custom_process_message(message):
    # print("Recivin messages")
    # df = pd.DataFrame(json_message)
    # frames.append(df)
    # df.to_excel("tble.xlsx", sheet_name="Sheet1")
    # print(type(json_message))
    # print(df.head)

    json_message = json.loads(message)

    # pprint.pprint(type(json_message))
    # pprint.pprint((json_message[0]))
    # pprint.pprint((json_message[0]['b']))
    # pprint.pprint(type(json_message[0]['t']))


    if sys.argv[2] == 'a':
        for lst in json_message[0]['a']:
            if json_message[0]['x'] == 1:
                data['Price'].append(lst[0])
                data['Volume'].append(lst[1])
    elif sys.argv[2] == 'b':
        for lst in json_message[0]['b']:
            if json_message[0]['x'] == 1:
                data['Price'].append(lst[0])
                data['Volume'].append(lst[1])
    else:
        print('pass a for ask, b for bid')


        # pprint.pprint(lst[1])


def my_custom_error_handler(ws, error):
    print("Error", error)


def my_custom_close_handler(ws):
    print("Closing")

def reportAsks(ew):
    sheet_num = 1
    start = 0
    end = 100
    for x in range(len(data['Price']) // 100):
        temp_dict = {}
        temp_dict['Price'] = data['Price'][start:end]
        temp_dict['Volume'] = data['Volume'][start:end]
        pd.DataFrame(temp_dict).to_excel(ew, sheet_name=f'sheet{sheet_num}')
        print(tabulate(temp_dict, headers='keys', tablefmt='psql'))
        print("------------------------printed asks------------------------")
        sheet_num += 1
        start = start + 100 - 1
        end = end + 100 - 1

def reportBids(ew):
    sheet_num = 1
    start = 0
    end = 100
    for x in range(len(data['Price']) // 100):
        temp_dict = {}
        temp_dict['Price'] = data['Price'][start:end]
        temp_dict['Volume'] = data['Volume'][start:end]
        pd.DataFrame(temp_dict).to_excel(ew, sheet_name=f'sheet{sheet_num}')
        print(tabulate(temp_dict, headers='keys', tablefmt='psql'))
        print('--------------------------DONE--------------------------')
        sheet_num += 1
        start = start + 100 - 1
        end = end + 100 - 1


def main():
    key = "IR69iir3RqApPUaedAHTSJ2UuTJ9ASlB"
    my_client = WebSocketClient(CRYPTO_CLUSTER, key, my_custom_process_message)
    my_client.run_async()

    my_client.subscribe(f"XL2.{sys.argv[1].upper()}-USD")
    time.sleep(0.5)

    my_client.close_connection()

    if sys.argv[2] == 'a':
        ew = pd.ExcelWriter(f'{sys.argv[1]}_ask.xlsx', engine="xlsxwriter", mode="w")
        reportAsks(ew)
        print(('-'*15) + 'Reported asks' + ('-'*15))

    elif sys.argv[2] == 'b':
        ew = pd.ExcelWriter(f'{sys.argv[1]}_bid.xlsx', engine="xlsxwriter", mode="w")
        reportBids(ew)
        print(('-'*15) + 'Reported bids' + ('-'*15))

    else:
        print('Enter a for ask, b for bid')


    # print(tabulate(data, headers='keys', tablefmt='psql'))
    print(f'Sending over {sys.argv[1].upper()}-USD data')
    print(len(data['Price']) // 100)

    ew.save()


if __name__ == "__main__":
    main()
