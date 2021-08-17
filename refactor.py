from polygon import WebSocketClient, CRYPTO_CLUSTER
import sys
import pprint
import time
import json
import pandas as pd
import pdb
from tabulate import tabulate
from matplotlib import pyplot as plt

current_price = 0.0
data_asks = {'Price': [0 for x in range(100)], 'Volume': [0 for x in range(100)]}
data_bids = {'Price': [0 for x in range(100)], 'Volume': [0 for x in range(100)]}
asks_weighted = {'Price': [0 for x in range(100)], 'Weight': [0 for x in range(100)]}
bids_weighted = {'Price': [0 for x in range(100)], 'Weight': [0 for x in range(100)]}
ready = False
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
sheetNum = 0
signals = []
plot_data = {'Time': [], 'Signal': []}
price_data = {'Time': [], 'Price': []}

def my_custom_process_message(message):
    global current_price
    global data_asks
    global data_bids
    global asks_weighted
    global bids_weighted
    global ready
    global sheetNum
    global signals
    global plot_data

    json_message = json.loads(message)[0] # Treats the json message like a python dict

    # Save the current price
    if json_message['ev'] == 'XT':
        current_price = float(json_message['p'])
        price_data['Time'].append(time.time())
        price_data['Price'].append((current_price))
        print(f'Recinivng current price data: {current_price}')


    # Once we have the price we are ready to operate on lv2 data, keep assignig lv2 data, so we stay up to date
    elif current_price != 0.0 and json_message['ev'] == 'XL2':
        print('Recinivng level 2 Book data')
        ready = True
        assignAsksBids(json_message)
        # assignWeights('a')
        # assignWeights('b')

    # For evry price after we are ready, we will operate as follows
    if json_message['ev'] == 'XT' and ready:
        sheetNum += 1
        assignWeights('a')
        assignWeights('b')
        plot_data['Time'].append((time.time()))
        plot_data["Signal"].append(genSignal())
        print('-'*25 + 'Operating on lv2 data' + '-'*25)
        # print('-'*25 + 'asks' + '-'*25)
        # print(tabulate(asks_weighted, headers='keys', tablefmt='grid'))
        writeToExcel(f'{current_price}_{sheetNum}')
        # print('-'*25 + 'bids' + '-'*25)
        # print(tabulate(bids_weighted, headers='keys', tablefmt='grid'))

    # elif json_message['ev'] == 'XL2' and ready:
    #     signals.append(signal := genSignal())
    #     plot_data['Time'].append(time.strftime("%I:%M:%S",time.gmtime(time.time())))
    #     plot_data["Signal"].append(signal)


def writeToExcel(sheetNum: str):
    global asks_weighted
    global writer

    df1 = pd.DataFrame(asks_weighted)
    df2 = pd.DataFrame(bids_weighted)
    df3 = pd.DataFrame(plot_data)

    df1.to_excel(writer, sheet_name=(sheetNum), index=False)
    df2.to_excel(writer, sheet_name=(sheetNum), index=False, startcol=3)
    df3.to_excel(writer, sheet_name=(sheetNum), index=False, startcol=7)

    workbook = writer.book
    worksheet = writer.sheets[sheetNum]
    worksheet.conditional_format('B2:B101', {'type': '3_color_scale'})
    worksheet.conditional_format('E2:E101', {'type': '3_color_scale'})

def plotData():
    global plot_data
    global price_data

    plt.figure()
    plt.subplot(211)
    plt.plot(plot_data['Time'], plot_data['Signal'], 'o-')

    plt.subplot(212)
    plt.plot(price_data['Time'], price_data['Price'], 'r--')
    # plt.xlabel('Time')
    # plt.ylabel('Signal')
    # plt.title('Signal Data')

    plt.show()

def assignAsksBids(json_message):
    global data_asks
    global data_bids
    global asks_weighted
    global bids_weighted

    if json_message['x'] == 1:
        i = 0
        for lst in json_message['b']:
            data_bids['Price'][i] = (lst[0])
            bids_weighted['Price'][i] = (lst[0])
            data_bids['Volume'][i] = (lst[1])
            i += 1
        i = 0
        for lst in json_message['a']:
            data_asks['Price'][i] = (lst[0])
            asks_weighted['Price'][i] = (lst[0])
            data_asks['Volume'][i] = (lst[1])
            i += 1

def diff(x,y):
    if x >= y:
        return abs((x - y) / x)

    return abs((y - x) / y)

def assignWeights(x: str):
    global asks_weighted
    global bids_weighted
    global data_asks
    global data_bids
    global current_price

    size = 100
    weights = [x / size for x in range(size)]

    if x == 'a':
        i = 0
        lst = []
        while i < size:
            lst.append(diff(current_price, asks_weighted['Price'][i]))
            i += 1

        i = 0
        while len(weights) > 0 and i < size:
            asks_weighted['Weight'][lst.index(min(lst))] = weights.pop()
            lst[lst.index(min(lst))] = 9999999.999

    elif x == 'b':
        i = 0
        lst = []
        while i < size:
            lst.append(diff(current_price, bids_weighted['Price'][i]))
            i += 1

        i = 0
        while len(weights) > 0 and i < size:
            bids_weighted['Weight'][lst.index(min(lst))] = weights.pop()
            lst[lst.index(min(lst))] = 9999999.999

    else:
        print('pass in a or b')

def genSignal():
    '''
    For each price in asks:
        -> take product of price volume and weight
        -> add it to a sum

    For each price in bids:
        -> take product of price volume and weight
        -> add it to a sum
    '''
    asks = 0
    bids = 0
    for i in range(100):
        product = data_asks['Price'][i] * data_asks['Volume'][i] * asks_weighted['Weight'][i]
        asks += product
        product = data_bids['Price'][i] * data_bids['Volume'][i] * bids_weighted['Weight'][i]
        bids += product

    return bids / asks

def my_custom_error_handler(ws, error):
    print("Error", error)

def my_custom_close_handler(ws):
    print("Closing")

def main():
    key = "IR69iir3RqApPUaedAHTSJ2UuTJ9ASlB"
    my_client = WebSocketClient(CRYPTO_CLUSTER, key, my_custom_process_message, my_custom_close_handler, my_custom_error_handler)
    my_client.run_async()

    my_client.subscribe(f"XT.{sys.argv[1].upper()}-USD", f"XL2.{sys.argv[1].upper()}-USD")
    # my_client.subscribe(f"XT.{sys.argv[1].upper()}-USD")
    time.sleep(60 * 5)

    my_client.close_connection()

    pprint.pp(plot_data)
    # print(F'Length of signlas is {len(signals)}')
    pprint.pp(price_data)

    plotData()


if __name__ == '__main__':
    main()
    writer.save()
