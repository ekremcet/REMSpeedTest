import socket
import string
import random
import time

FILE_SIZE = 25000000
ONE_MB = 1000000
BUFFER_SIZE = 4096


class Client:
    def __init__(self, ip_addr, port):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_addr = ip_addr
        self.port = port
        self.ping_msg = self.generate_random_data(64)

    def connect_to_server(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.connect((self.ip_addr, self.port))

    def send_ping(self):
        self.server_sock.send(self.ping_msg.encode("ascii"))
        self.server_sock.recv(BUFFER_SIZE)

    @staticmethod
    def generate_random_data(size):
        alphabet = string.ascii_uppercase + string.ascii_lowercase

        return ''.join(random.choice(alphabet) for _ in range(size))

    def download_test(self):
        self.server_sock.send("Down".encode("ascii"))
        t1 = time.time()
        bytes_recieved = 0
        with open("./tmpupload", "wb") as f:
            while True:
                data = self.server_sock.recv(BUFFER_SIZE)
                bytes_recieved += len(data)
                f.write(data)
                if bytes_recieved >= FILE_SIZE:
                    break

        t2 = time.time()
        download_speed = round(((FILE_SIZE * 0.001) / (t2 - t1)) * 0.001) * 8
        self.server_sock.send(str(download_speed).encode("ascii"))
        print("Download test complete")

    def upload_test(self):
        self.server_sock.send("Upld".encode("ascii"))
        test_file = open("./uploadfile", "rb")
        buff = test_file.read()
        # Send the file to client
        while buff:
            self.server_sock.send(buff)
            buff = test_file.read()
        test_file.close()
        print("Upload test complete")

    def ping_test(self):
        self.server_sock.send("Ping".encode("ascii"))
        for _ in range(10):
            self.send_ping()

    def run_tests(self):
        self.connect_to_server()
        self.ping_test()
        self.connect_to_server()
        self.download_test()
        self.connect_to_server()
        self.upload_test()
        self.server_sock.close()


if __name__ == '__main__':
    client = Client('13.80.2.211', 33333)
    client.run_tests()