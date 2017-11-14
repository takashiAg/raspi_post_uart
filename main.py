# encoding:UTF-8

import serial
import urllib
import threading

# POSTするURL
url = "http://html.takashia.xyz/post.php"

# シリアルポートを指定
serport = "/dev/serial0"


def post(arg):
    # 受信したデータを;でわける
    message = arg.split(";")
    try:
        error_checker = message[9]
        # tweliteから送られてきた情報が送信すべき情報であれば送信
    except IndexError:
        print("too short message")
        return 0
    except:
        print("unknown error")
        return 0
    try:
        params = {'uart': arg}
        data = urllib.urlencode(params)
        urllib.urlopen(url, data)
        print("I send a message to " + url + "\nmessage:" + arg)
        return 0
    except:
        print("I try to send a message but missed it")
        return 0
    return 0


# main program
# シリアル通信を開始


def main():
    port = serial.Serial(serport, 115200)
    while True:
        try:
            rcv = port.readline()
            resp = rcv.strip()
            print(resp)
            # データを送信する。送信中にシリアルからのアクセスが来て時間が遅れてしまうのを避けるため新しいスレッドを立てる
            threading.Thread(target=post, args=(resp,)).start()
        except:
            print("error")


if __name__ == "__main__":
    main()
