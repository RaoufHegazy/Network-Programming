import socket
import threading


class Server:
    def __init__(self):
        print("Setting up server...")
        self.address = '127.0.0.1'
        self.port = 8000
        self.active_connections = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.address, self.port))
        self.socket.listen()

        self.clients = {}
        self.players = []
        self.initial_turn = True

    def start(self):
        print("Starting server...")
        while True:
            client, client_address = self.socket.accept()
            try:
                print("------------------------------------------------------------------------")
                print("Client {0}:{1} connected.".format(client_address[0], client_address[1]))
                self.active_connections += 1
                print("Current connections: {}".format(str(self.active_connections)))
            except:
                print("passing")
            client_handler = threading.Thread(target=self.handle_client, args=(client, client_address))
            client_handler.start()
            print("new thread started")

    def end(self):
        print("Stopping server...")
        self.socket.close()

    def handle_client(self, connection, client_info):
        client_id = self.active_connections
        print("-----CLIENTID: ", client_id)
        assigned_players = self.assign_player(connection, client_id)
        self.clients[client_id] = connection

        if self.active_connections > 1 and assigned_players:
            self.server_message("start")

        client_nickname = "guest_" + str(self.active_connections)

        client_ip, client_port = client_info

        while True:
            try:
                request = connection.recv(4096)
            except:
                print("AN ERROR OCCURRED. Breaking out of loop.")
                break

            if not request:
                print("BREAKING")
                break

            # got column number
            try:
                received = request.decode('UTF-8').strip()
                if "/play" in received:
                    self.players.append(client_nickname)
                elif received == '/online':
                    self.server_message("There are currently {} user(s) connected\n".format(self.active_connections))
                elif received == '/ping':
                    self.server_message("PONG\n")
                elif received.startswith('winner'):
                    winner = received.split('=')[1]
                    print("winner:::::::::::::::")
                    print(winner)
                    self.server_message(request)
                elif received == '/exit':
                    break
            except:
                # means we're getting byte data
                received = request
                self.send_server_payload(request)

            print("Got: ", received)

        self.active_connections -= 1
        if not self.clients.pop(client_id, None):
            print("key not found")

        connection.close()

        print("Client {0}:{1} left. Current connections: {2}".format(client_ip, client_port, self.active_connections))

    def send_server_payload(self, payload):
        print("Sending payload..")
        for client_id, connection in self.clients.items():
            connection.send(payload)

    def server_message(self, msg):
        print("Sending server message ({}) to:".format(msg), self.clients)
        for client_id, connection in self.clients.items():
            connection.send(msg.encode())

    def private_message(self, client_id, msg):
        self.clients[client_id].send(msg)

    def global_message(self, nickname, message):
        msg = "{0} wrote: {1}\n".format(nickname, message)
        self.server_message(msg)

    def set_client_nickname(self, user_command):
        try:
            return user_command.split()[1]
        except:
            return None

    def assign_player(self, connection, client_id):
        print("assigning player, sending message: {}".format(str(client_id)))
        msg = str(client_id).encode()
        connection.send(msg)
        return True


serv = Server(10)
serv.start()