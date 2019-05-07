import socket
import sys
import time
from _thread import start_new_thread

MAX_BYTES = 1500
TEN_MB = 10500000

class Server:
    def __init__(self, ip_addr, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_addr = ip_addr

    def start_server(self):
        self.sock.bind((self.server_addr, self.port))
        self.sock.listen(5)
        while True:
            print("Waiting for connections..")
            client, client_addr = self.sock.accept()
            print("Connected to: " + str(client_addr[0]) + ":" + str(client_addr[1]))
            start_new_thread(self.client_thread, (client, ))
        self.sock.close()

    def get_delay(self, client):
        rtt = 0.0
        for _ in range(10):
            rtt += self.get_pings(client)
        ping = rtt / 10
        print("Ping: %.2f" % ping)

        return ping

    @staticmethod
    def get_pings(client):
        send_time = time.time()
        msg = client.recv(MAX_BYTES)
        client.send(msg)
        recv_time = time.time()

        return (recv_time - send_time) * 1000

    @staticmethod
    def get_download_speed(client):
        file10mb = open("./10mb.bin", "rb")
        buff = file10mb.read()
        # Send the file to client
        while buff:
            client.send(buff)
            buff = file10mb.read()
        client.send(b'\x10')  # Close signal for file
        file10mb.close()
        download_speed = client.recv(1024).decode("ascii")
        print("Download speed %s Mbps" % download_speed)

        return download_speed

    @staticmethod
    def get_upload_speed(client):
        with open("./10mbuploaded", "wb") as f:
            t1 = time.time()
            while True:
                data = client.recv(1024)
                if data == b'\x10':
                    break
                f.write(data)

            t2 = time.time()
            upload_speed = str(round(((TEN_MB * 0.001) / (t2 - t1)) * 0.001))
            print("Upload speed: %s Mbps" % upload_speed)

            return upload_speed

    def client_thread(self, client):
        while True:
            self.get_delay(client)
            self.get_download_speed(client)
            self.get_upload_speed(client)
            break
        client.close()


if __name__ == '__main__':
    server = Server("10.200.49.116", 12501)
    server.start_server()
