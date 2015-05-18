from threading import Thread

class ClientContext(Thread):
    def __init__(self, client_socket, on_message, on_close):
        self.sock = client_socket
        self.on_message = on_message
        self.on_close = on_close
        self.started = False
        Thread.__init__(self)
        
    def send(self, message):
        self.sock.sendall(message.encode("utf-8"))

    def stop(self):
        self.started = False 

    def run(self):
        if self.started:
            return

        self.started = True
        while self.started:
            message = str(self.sock.recv(4096))

            if len(message) > 0:
                self.on_message(message)
            else:
                self.on_close("SOCKET ERROR")
                return

        return

