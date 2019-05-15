import sys
import string
import random
import time
from websocket_server import WebsocketServer

FILE_SIZE = 10000000


class Server:
    def __init__(self, ip_addr, port):
        self.sock = WebsocketServer(port=port, host=ip_addr)
        self.server_addr = ip_addr
        #self.generate_file()

    def generate_file(self):
        # Generate 10 MB file with random strings in each run
        # This is done to prevent caching
        data = self.generate_random_data(FILE_SIZE)
        with open("./downfile", "w") as f:
            f.write(data)

    def start_server(self, type):
        if type == "D":
            self.sock.set_fn_new_client(self.download_thread)
        elif type == "U":
            self.sock.set_fn_new_client(self.upload_thread)
        elif type == "P":
            self.sock.set_fn_new_client(self.delay_thread)
        self.sock.run_forever()

    def get_delay(self, client):
        # Client sends a packet to server, server sends back a packet as soon as it receives that packet
        # Time passed between 2 received packets are calculated and divided by two to obtain RTT
        # This process is repeated 10 times to obtain more reliable results
        print("Delay Test")
        self.sock.set_fn_message_received(self.get_ping)

    def get_ping(self, client, server, message):
        self.sock.send_message(client, self.generate_random_data(64))

    @staticmethod
    def generate_random_data(size):
        # Generate random string with given size in bytes
        alphabet = string.ascii_uppercase + string.ascii_lowercase

        return ''.join(random.choice(alphabet) for _ in range(size))

    def get_download_speed(self, client):
        # Send a 10MB randomly generated file to client
        # Speed calculation is done in client side
        print("Download Test")
        download_file = open("./downfile", "rb")
        buff = download_file.read()
        # Send the file to client
        while buff:
            self.sock.send_message(client, buff)
            buff = download_file.read()
        print("Test Complete")
        download_file.close()

    def upload_control(self, client, server, message):
        self.bytes_received += len(message)
        if self.bytes_received >= FILE_SIZE:
            t2 = time.time()
            self.sock.send_message(client, str(t2 - self.t1))

    def get_upload_speed(self, client):
        # Receive a 10MB randomly generated data from client
        # Speed calculation is done in client side
        print("Upload Test")
        self.bytes_received = 0
        self.t1 = time.time()
        self.sock.set_fn_message_received(self.upload_control)

    def delay_thread(self, client, server):
        self.get_delay(client)

    def download_thread(self, client, server):
        self.get_download_speed(client)

    def upload_thread(self, client, server):
        self.get_upload_speed(client)


if __name__ == '__main__':
    upload_server = Server("0.0.0.0", int(sys.argv[1]))
    upload_server.start_server(type=sys.argv[2])
