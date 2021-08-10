# from os import times
import time
import json
# import pprint
import pandas as pd
import sys
import xlsxwriter

from tabulate import tabulate
from pandas.core.frame import DataFrame
from pandas import ExcelWriter
from polygon import WebSocketClient, CRYPTO_CLUSTER

# frames = []
data_asks = {"Price": [], "Volume": []}
data_bids = {"Price": [], "Volume": []}
weights = [x / 100 for x in range(100)]

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
                data_asks['Price'].append(lst[0])
                data_asks['Volume'].append(lst[1])

    elif sys.argv[2] == 'b':
        for lst in json_message[0]['b']:
            if json_message[0]['x'] == 1:
                data_bids['Price'].append(lst[0])
                data_bids['Volume'].append(lst[1])

    elif sys.argv[2] == 'both':
        if json_message[0]['x'] == 1:
            for lst1 in json_message[0]['b']:
                data_bids['Price'].append(lst1[0])
                data_bids['Volume'].append(lst1[1])
            for lst2 in json_message[0]['a']:
                data_asks['Price'].append(lst2[0])
                data_asks['Volume'].append(lst2[1])

    else:
        print('pass a for ask, b for bid, both for ask and bids')

        # pprint.pprint(lst[1])


def my_custom_error_handler(ws, error):
    print("Error", error)


def my_custom_close_handler(ws):
    print("Closing")


def reportAsks(ew):
    sheet_num = 1
    start = 0
    end = 100
    for x in range(len(data_asks['Price']) // 100):
        temp_dict = {}
        temp_dict['Price'] = data_asks['Price'][start:end]
        temp_dict['Volume'] = data_asks['Volume'][start:end]
        pd.DataFrame(temp_dict).to_excel(ew, sheet_name=f'sheet{sheet_num}', index=False)
        print(tabulate(temp_dict, headers='keys', tablefmt='psql'))
        print("------------------------DONE------------------------")
        sheet_num += 1
        start = start + 100
        end = end + 100

def reportBids(ew):
    sheet_num = 1
    start = 0
    end = 100
    for x in range(len(data_bids['Price']) // 100):
        temp_dict = {}
        temp_dict['Price'] = data_bids['Price'][start:end]
        temp_dict['Volume'] = data_bids['Volume'][start:end]
        pd.DataFrame(temp_dict).to_excel(ew, sheet_name=f'sheet{sheet_num}', index=False)
        print('--------------------------DONE--------------------------')
        sheet_num += 1
        start = start + 100
        end = end + 100


def reportBidsAsks(ew):
    sheet_num = 1
    start = 0
    end = 100
    # workbook = ew.book
    # worksheet = ew.sheets[f'Sheet{sheet_num}']

    for x in range(len(data_asks['Price']) // 100):

        temp_dict1 = {}
        temp_dict1['Price'] = data_asks['Price'][start:end]
        temp_dict1['Volume'] = data_asks['Volume'][start:end]
        print(('-'*15)+'asks'+('-'*15))
        print(tabulate(temp_dict1, headers='keys', tablefmt='psql'))
        pd.DataFrame(temp_dict1).to_excel(ew, sheet_name=f'Sheet{sheet_num}', index=False)

        temp_dict2 = {}
        temp_dict2['Price'] = data_bids['Price'][start:end]
        temp_dict2['Volume'] = data_bids['Volume'][start:end]
        print(('-'*15)+'bids'+('-'*15))
        print(tabulate(temp_dict2, headers='keys', tablefmt='psql'))
        pd.DataFrame(temp_dict2).to_excel(ew, sheet_name=f'Sheet{sheet_num}', startcol=3, index=False)

        sheet_num += 1
        start = start + 100
        end = end + 100

def main():
    key = "IR69iir3RqApPUaedAHTSJ2UuTJ9ASlB"
    my_client = WebSocketClient(CRYPTO_CLUSTER, key, my_custom_process_message)
    my_client.run_async()

    my_client.subscribe(f"XL2.{sys.argv[1].upper()}-USD")
    time.sleep(float(sys.argv[3]))

    my_client.close_connection()


    if sys.argv[2] == 'a':
        ew = pd.ExcelWriter(f'{sys.argv[1]}_ask.xlsx', engine="xlsxwriter", mode="w")
        reportAsks(ew)
        print(len(data_asks['Price']) // 100)
        print(('-'*15) + 'Reported asks' + ('-'*15))

    elif sys.argv[2] == 'b':
        ew = pd.ExcelWriter(f'{sys.argv[1]}_bid.xlsx', engine="xlsxwriter", mode="w")
        reportBids(ew)
        print(len(data_bids['Price']) // 100)
        print(('-'*15) + 'Reported bids' + ('-'*15))

    elif sys.argv[2] == 'both':
        ew = pd.ExcelWriter(f'{sys.argv[1]}_bid_ask.xlsx', engine="xlsxwriter", mode="w")
        print('ask len:', len(data_asks['Price']) // 100)
        print('bid len:', len(data_bids['Price']) // 100)
        reportBidsAsks(ew)

    else:
        print('Enter a for ask, b for bid, both for asks and bids')


    # print(tabulate(data, headers='keys', tablefmt='psql'))
    print(f'Sending over {sys.argv[1].upper()}-USD data')

    ew.save()


if __name__ == "__main__":
    main()
