import socket
import string
import random
import time
from _thread import start_new_thread

FILE_SIZE = 25000000
BUFFER_SIZE = 4096


class Server:
    def __init__(self, ip_addr, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_addr = ip_addr
        self.generate_file()

    def generate_file(self):
        # Generate 25 MB file with random strings in each run
        # This is done to prevent caching
        data = self.generate_random_data(FILE_SIZE)
        with open("./downfile", "wb") as f:
            f.write(data.encode("ascii"))

    def start_server(self):
        self.sock.bind((self.server_addr, self.port))
        self.sock.listen(5)
        while True:
            print("Waiting for connections..")
            client, client_addr = self.sock.accept()
            print("Connected to: " + str(client_addr[0]) + ":" + str(client_addr[1]))
            start_new_thread(self.client_thread, (client, ))

    def get_delay(self, client):
        # Client sends a packet to server, server sends back a packet as soon as it receives that packet
        # Time passed between 2 received packets are calculated and divided by two to obtain RTT
        # This process is repeated 10 times to obtain more reliable results
        print("Delay Test")
        rtt = 0.0
        for _ in range(10):
            rtt += self.get_pings(client)
        ping = rtt / 20
        client.send(str(round(ping)).encode("ascii"))

    @staticmethod
    def get_pings(client):
        t1 = time.time()
        msg = client.recv(BUFFER_SIZE)
        client.send(msg)
        t2 = time.time()

        return (t2 - t1) * 1000

    @staticmethod
    def generate_random_data(size):
        # Generate random string with given size in bytes
        alphabet = string.ascii_uppercase + string.ascii_lowercase

        return ''.join(random.choice(alphabet) for _ in range(size))

    @staticmethod
    def get_download_speed(client):
        # Send a 25MB randomly generated file to client
        # Speed calculation is done in client side
        print("Download Test")
        download_file = open("./downfile", "rb")
        buff = download_file.read()
        # Send the file to client
        while buff:
            client.send(buff)
            buff = download_file.read()

        download_file.close()

    @staticmethod
    def get_upload_speed(client):
        # Receive a 25MB randomly generated file from client
        # Speed calculation is done in server side and then sent to client
        print("Upload Test")
        bytes_recieved = 0
        t1 = time.time()
        while True:
            data = client.recv(BUFFER_SIZE)
            bytes_recieved += len(data)
            if bytes_recieved >= FILE_SIZE:
                break

        t2 = time.time()
        upload_speed = str(round(((FILE_SIZE / (t2 - t1)) * 0.000001) * 8))
        client.send(str(upload_speed).encode("ascii"))

    def client_thread(self, client):
        # First 4 bytes in connection is the test type
        request = client.recv(4).decode("ascii")
        requests = {"Ping": self.get_delay,
                    "Down": self.get_download_speed,
                    "Upld": self.get_upload_speed}
        requests[request](client)
        client.shutdown(socket.SHUT_RDWR)
        client.close()


if __name__ == '__main__':
    server = Server("0.0.0.0", 33333)
    server.start_server()
