import time

from polygon import WebSocketClient, CRYPTO_CLUSTER


def my_custom_process_message(message):
    print("this is my custom message processing", message)


def my_custom_error_handler(ws, error):
    print("this is my custom error handler", error)


def my_custom_close_handler(ws):
    print("this is my custom close handler")


def main():
    key = 'IR69iir3RqApPUaedAHTSJ2UuTJ9ASlB'
    my_client = WebSocketClient(CRYPTO_CLUSTER, key, my_custom_process_message)
    my_client.run_async()

    a = my_client.subscribe("XL2.DOGE-USD")
    time.sleep(1)

    my_client.close_connection()

    print('a is {}',my_client)


if __name__ == "__main__":
    main()
