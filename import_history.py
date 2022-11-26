import socket
import os

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5006))
print("成功连接.....")


def send_file(filepath):
    if not os.path.exists(filepath):
        print('文件不存在')
        exit(0)
    filesize = os.path.getsize(filepath)
    client.send(f"{filepath}{SEPARATOR}{filesize}".encode())
    print('文件发送中...')
    with open(filepath, 'rb')as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client.send(bytes_read)

    # client.send(FILEEND_MARK.encode())
    print('文件发送完成，等待处理...')


def receive_log():
    while True:
        data = client.recv(BUFFER_SIZE)
        print(data.decode())


def main():
    filepath = input('输入历史记录文件:\n')
    send_file(filepath)
    receive_log()


main()
