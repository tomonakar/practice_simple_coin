from concurrent.futures import ThreadPoolExecutor
import socket
import os


def __handle_message(args_tuple):

    conn, addr, data_sum = args_tuple
    while True:
        data = conn.recv(1024)
        data_sum = data_sum + data.decode('utf8')

        if not data:
              break

        if data_sum != '':
            print(data_sum)


def __get_myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


def main():

    # AF_INET : IPv4 ベースのアドレス体系を使う
    # SOCK_STREAM : TCP/IP を使う
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 多重接続になっても良いようにスレッドで処理するようにする
    executor = ThreadPoolExecutor(max_workers=os.cpu_count())
    print('cpu_count', os.cpu_count())

    # 開くポート番号は適当
    myhost = __get_myip()
    print('my ip address is now ...', myhost)
    my_socket.bind((myhost, 50030))
    # 同時に接続してくる相手の数。今回はテストで１とする
    my_socket.listen(1)

    while True:
        # 接続があるまで待機
        print('Waiting for the connection...')
        conn, addr = my_socket.accept()
        print('Connect by ...', addr)
        data_sum = ''
        executor.submit(__handle_message, (conn, addr, data_sum))


if __name__ == '__main__':
    main()