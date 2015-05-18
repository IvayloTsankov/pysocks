import socket


class Client:
    def __init__(self, on_open, on_message, on_close):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.on_open = on_open
        self.on_message = on_message
        self.on_close = on_close

    def connect(self, host, port):
        self.host = host
        self.port = port
        try:
            server_ip = socket.gethostbyname(host)
            print("SERVER({}) IP IS {}".format(host, server_ip))
            self.sock.connect((server_ip, port))
            self.connected = True
        except socket.error as msg:
            print(msg)
            self.close()
            return

        self.on_open(host, port)

    def send(self, message):
        self.sock.sendall(message.encode("ascii"))

    def start_interactive(self):
        if not self.connected:
            return

        while self.connected:
            user_input = input("Insert message: ")
            print(user_input)
            try:
                self.send(user_input)
            except socket.error as msg:
                print("SEND FAILED")
                return

            message = self.sock.recv(4096)

            if len(message) != 0:
                self.on_message(message)
            else:
                self.close()

    def close(self, reason=""):
        self.sock.close()
        self.connected = False
        self.on_close(reason)


def on_open(host, port):
    print("Client connected to {} {}".format(host, port))

def on_message(message):
    print("ON MESSAGE {}".format(message))

def on_close(reason):
    print("ON CLOSE {}".format(reason))


if __name__ == "__main__":
    client = Client(on_open, on_message, on_close)
    host = input("host: ")
    port = int(input("port: "))

    client.connect(host, port)
    client.start_interactive()
