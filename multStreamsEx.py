from polygon import WebSocketClient, CRYPTO_CLUSTER
import sys
import pprint
import time
import json
from tabulate import tabulate

current_price = 0.0
data_asks = {'Price': [], 'Volume': []}
data_bids = {'Price': [], 'Volume': []}


def my_custom_process_message(message):

    global current_price
    asks_weighted = {'Price': [], 'Weight': [0 for x in range(100)]}
    bids_weighted = {'Price': [], 'Weight': [0 for x in range(100)]}
    weights = [x / 100 for x in range(100)]
    # print(tabulate(json_message['a'], headers=['Price', 'Volume'], tablefmt='fancy_grid'))

    json_message = json.loads(message)[0]

    print(json_message['ev'])

    if json_message['ev'] == 'XT':
        current_price = float(json_message['p'])
        print(f'current price is {(current_price)}')

    elif float(current_price) != 0.0 and json_message['ev'] == 'XL2':
        assignAsksBids(json_message)
        # print('-'*25 + 'asks' + '-'*25)
        # printTble('a', 'fancy_grid', data_asks)
        # print('-'*25 + 'bids' + '-'*25)
        # printTble('b', 'fancy_grid', data_bids)
        # print('sainity')
        assignWeights(json_message, 'a', asks_weighted, weights)
        # printTble('a', 'fancy_grid', asks_weighted)
        pprint.pprint(asks_weighted)
        print('-'*25 + 'Weighted Asks' + '-'*25)

def assignWeights(json_message, x: str, tble: dict, weights: list):
    global data_bids
    global data_asks
    global current_price

    if x == 'a' and json_message['x'] == 1:

        # printTble('a', 'fancy_grid', data_asks)
        lst = []
        for price in data_asks['Price']:
            # print(f'sainity: price / current_price: {price / current_price}')
            lst.append(price / current_price)
            # print(f'sainity: size of lst: {len(lst)}')
            tble['Price'].append(price)

        i = 0
        while i < len(lst):
            tble['Weight'][lst.index(min(lst))] = weights.pop()

    elif x == 'b' and json_message['x'] == 1:

        for price in data_bids['price']:
            if 0.0 < (price - current_price) and (price - current_price) < 1.0:
               tble['Price'].append(price)
               tble['Weight'].append(weights.pop())


def assignAsksBids(json_message):
    global data_bids
    global data_asks
    # print((json_message['b']))
    if json_message['x'] == 1:
        for lst in json_message['b']:
            data_bids['Price'].append(lst[0])
            data_bids['Volume'].append(lst[1])
        for lst in json_message['a']:
            data_asks['Price'].append(lst[0])
            data_asks['Volume'].append(lst[1])

def printTble(x: str, frmt: str, tble: dict):
    global data_asks
    global data_bids
    start = 0
    end = 100
    # print(f'sainity {(list(tble.keys())[0])}')
    if x == 'a':
        for i in range(len(tble[list(tble.keys())[0]]) // 100):
            temp_dict = {}
            temp_dict[list(tble.keys())[0]] = tble[list(tble.keys())[0]][start:end]
            temp_dict[list(tble.keys())[1]] = tble[list(tble.keys())[1]][start:end]
            print(tabulate(temp_dict, headers='keys', tablefmt=frmt))
            start = start + 100
            end = end + 100

    elif x == 'b':
        for i in range(len(tble[tble.keys()[0]]) // 100):
            temp_dict = {}
            temp_dict[list(tble.keys())[0]] = tble[list(tble.keys())[0]][start:end]
            temp_dict[list(tble.keys())[1]] = tble[list(tble.keys())[1]][start:end]
            print(tabulate(temp_dict, headers='keys', tablefmt=frmt))
            start = start + 100
            end = end + 100
    else:
        print('pass in a or b bro')



def my_custom_error_handler(ws, error):
    print("Error", error)


def my_custom_close_handler(ws):
    print("Closing")

def jusGo(x):

    key = "IR69iir3RqApPUaedAHTSJ2UuTJ9ASlB"
    my_client = WebSocketClient(CRYPTO_CLUSTER, key, my_custom_process_message, my_custom_close_handler, my_custom_error_handler)
    my_client.run_async()

    my_client.subscribe(f"XT.{x.upper()}-USD", f"XL2.{x.upper()}-USD")
    # my_client.subscribe(f"XT.{sys.argv[1].upper()}-USD")
    time.sleep(1)

    my_client.close_connection()

def main():

    key = "IR69iir3RqApPUaedAHTSJ2UuTJ9ASlB"
    my_client = WebSocketClient(CRYPTO_CLUSTER, key, my_custom_process_message, my_custom_close_handler, my_custom_error_handler)
    my_client.run_async()

    my_client.subscribe(f"XT.{sys.argv[1].upper()}-USD", f"XL2.{sys.argv[1].upper()}-USD")
    # my_client.subscribe(f"XT.{sys.argv[1].upper()}-USD")
    time.sleep(1)

    my_client.close_connection()

if __name__ == '__main__':
    main()
