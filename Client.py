import socket
import string
import random
import time

FILE_SIZE = 25000000
BUFFER_SIZE = 4096


class Client:
    def __init__(self, ip_addr, port):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_addr = ip_addr
        self.port = port
        # Generate a random 64 Byte data for delay test
        self.ping_msg = self.generate_random_data(64)

    def connect_to_server(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.connect((self.ip_addr, self.port))

    def send_ping(self):
        # Send 64 Byte packet to server and receive response
        self.server_sock.send(self.ping_msg.encode("ascii"))
        self.server_sock.recv(BUFFER_SIZE)

    @staticmethod
    def generate_random_data(size):
        alphabet = string.ascii_uppercase + string.ascii_lowercase

        return ''.join(random.choice(alphabet) for _ in range(size))

    def download_test(self):
        # First send test type header to server then
        # Download the data from server and write it to file
        # The file will be used for upload speed testing
        self.server_sock.send("Down".encode("ascii"))
        t1 = time.time()
        bytes_recieved = 0
        with open("./uploadfile", "wb") as f:
            while True:
                data = self.server_sock.recv(BUFFER_SIZE)
                bytes_recieved += len(data)
                f.write(data)
                if bytes_recieved >= FILE_SIZE:
                    break

        t2 = time.time()
        # Download speed -> (FILE_SIZE_IN_BYTES / TIME_PASSED)
        # Divide it by 10^6 to convert it from Bytes per second to MBps
        # Multiply by 8 to convert it from MBps to Mbps
        download_speed = round(((FILE_SIZE / (t2 - t1)) * 0.000001) * 8)
        print("Download test complete")

        return download_speed

    def upload_test(self):
        # First send the test type header to server and send the downloaded file
        # Once the file is sent receive upload speed from server
        self.server_sock.send("Upld".encode("ascii"))
        test_file = open("./uploadfile", "rb")
        buff = test_file.read()
        # Send the file to client
        while buff:
            self.server_sock.send(buff)
            buff = test_file.read()
        test_file.close()
        upload_speed = self.server_sock.recv(BUFFER_SIZE).decode("ascii")
        print("Upload test complete")

        return upload_speed

    def ping_test(self):
        self.server_sock.send("Ping".encode("ascii"))
        for _ in range(10):
            self.send_ping()
        ping = self.server_sock.recv(BUFFER_SIZE).decode("ascii")
        print("Ping test complete")

        return ping

    def run_tests(self):
        # Initialize new connection for each test to obtain more reliable results
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