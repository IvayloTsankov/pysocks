import socket
import client_context


class SocketServer:
    def __init__(self, port, max_connections):
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.max_connections = max_connections
        self.clients = {}
        self.started = False

    def start(self, on_connect, on_message, on_close):
        print("SERVER LISTEN ON {}".format(self.port))
        self.listen_sock.bind(('', self.port))
        self.listen_sock.listen(self.max_connections)
        self.started = True

        while self.started:
            print("Accepting")
            (client_socket, address) = self.listen_sock.accept()
            client = client_context.ClientContext(client_socket, on_message, on_close)
            self.clients[client_socket] = client
            on_connect(client_socket, address)
            client.start()
         
    def stop(self):
        self.started = False

    def close_all(self):
        self.listen_sock.close()
        any(client.stop() for client in self.client.values())
        any(client.close() for client in self.clients.key())

    def send(self, client, message):
        try:
            self.client[client].send(message)
        except socket.error as msg:
            print(msg)


def on_connect(client, address):
    print("ON CONNECT {} {}".format(client, address))


def on_message(message):
    print("ON MESSAGE {}".format(message))


def on_close(reason):
    print("ON CLOSE {}".format(reason))


if __name__ == "__main__":
    port = int(input("Start on port: "))
    server = SocketServer(port, 5)
    server.start(on_connect, on_message, on_close)

