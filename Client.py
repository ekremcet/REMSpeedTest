import socket
import time

ping_message = "REMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMREMR"
TEN_MB = 10500000


class Client:
    def __init__(self, ip_addr, port):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.connect((ip_addr, port))

    def send_ping(self):
        self.server_sock.send(ping_message.encode("ascii"))
        self.server_sock.recv(1024)

    def download_test(self):
        with open("./10mbfile", "wb") as f:
            t1 = time.time()
            while True:
                data = self.server_sock.recv(1024)
                if data == b'\x10':
                    break
                f.write(data)

            t2 = time.time()
            download_speed = round(((TEN_MB * 0.001) / (t2 - t1)) * 0.001)
            self.server_sock.send(str(download_speed).encode("ascii"))
            print("Download test complete")

    def upload_test(self):
        file10mb = open("./10mbfile", "rb")
        buff = file10mb.read()
        # Send the file to client
        t1 = time.time()
        while buff:
            self.server_sock.send(buff)
            buff = file10mb.read()
        self.server_sock.send(b'\x10')  # Close signal
        file10mb.close()
        t2 = time.time()
        upload_speed = round(((TEN_MB * 0.001) / (t2 - t1)) * 0.001)
        print("Upload test complete")

    def ping_test(self):
        for _ in range(10):
            self.send_ping()

    def run_tests(self):
        self.ping_test()
        self.download_test()
        self.upload_test()
        self.server_sock.close()


if __name__ == '__main__':
    client = Client('10.200.49.116', 12501)
    client.run_tests()