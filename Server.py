import socket
import string
import random
import time
from _thread import start_new_thread

FILE_SIZE = 25000000
BUFFER_SIZE = 4096
ONE_MB = 1000000


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
        # Client sends a packet to server, server sends back a packet as soon as it recieves that
        # Time passed between 2 received packets are calculated and divided by two to obtain RTT
        # This process is repeated 10 times
        print("Delay Test")
        rtt = 0.0
        for _ in range(10):
            rtt += self.get_pings(client)
        ping = rtt / 20
        print("Ping: %.2f" % ping)

        return ping

    @staticmethod
    def get_pings(client):
        send_time = time.time()
        msg = client.recv(BUFFER_SIZE)
        client.send(msg)
        recv_time = time.time()

        return (recv_time - send_time) * 1000

    @staticmethod
    def generate_random_data(size):
        alphabet = string.ascii_uppercase + string.ascii_lowercase

        return ''.join(random.choice(alphabet) for _ in range(size))

    @staticmethod
    def get_download_speed(client):
        print("Download Test")
        download_file = open("./downfile", "rb")
        buff = download_file.read()
        # Send the file to client
        while buff:
            client.send(buff)
            buff = download_file.read()

        download_file.close()
        download_speed = client.recv(BUFFER_SIZE).decode("ascii")
        print("Download speed %s Mbps" % download_speed)

        return download_speed

    @staticmethod
    def get_upload_speed(client):
        print("UPLOAD")
        bytes_recieved = 0
        t1 = time.time()
        while True:
            data = client.recv(BUFFER_SIZE)
            bytes_recieved += len(data)
            if bytes_recieved >= FILE_SIZE:
                break

        t2 = time.time()
        upload_speed = str(round(((FILE_SIZE * 0.001) / (t2 - t1)) * 0.001) * 8)
        print("Upload speed: %s Mbps" % upload_speed)

        return upload_speed

    def client_thread(self, client):
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
