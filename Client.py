import socket
import time

ping_message = "REMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMR"
TEN_MB = 10500000


def send_ping(s):
    s.send(ping_message.encode("ascii"))
    s.recv(1024)


def receive_file(s):
    with open("./10mbfile", "wb") as f:
        t1 = time.time()
        while True:
            data = s.recv(1024)
            if data == b'\x10':
                break
            f.write(data)

        t2 = time.time()
        download_speed = round(((TEN_MB * 0.001) / (t2 - t1)) * 0.001)
        s.send(str(download_speed).encode("ascii"))
        print("Download test complete")

def send_file(s):
    file10mb = open("./10mbfile", "rb")
    buff = file10mb.read()
    # Send the file to client
    t1 = time.time()
    while buff:
        s.send(buff)
        buff = file10mb.read()
    s.send(b'\x10')  # Close signal
    file10mb.close()
    t2 = time.time()
    upload_speed = round(((TEN_MB * 0.001) / (t2 - t1)) * 0.001)
    print("Upload test complete")


def Main():
    host = '10.200.49.116'
    port = 12501
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        for _ in range(10):
            send_ping(s)
        receive_file(s)
        send_file(s)
        break
    s.close()


if __name__ == '__main__':
    Main()