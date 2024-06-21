import socket
import threading
import json
from databases.database import Database
from handlers.admin_handler import AdminHandler

class Server:
    def __init__(self, host='127.0.0.1', port=8889):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        self.db = Database()
        self.admin_handler = AdminHandler(self.db)

    def handle_client(self, client_socket):
        try:
            while True:
                message = client_socket.recv(4096).decode()
                if not message:
                    break
                data = json.loads(message)
                command = data['command']
                response = self.route_command(command, data['data'])
                client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def route_command(self, command, data):
        if command == 'authenticate':
            return self.authenticate(data['username'], data['password'])
        elif command == 'add_dish':
            return self.admin_handler.add_dish(data)
        elif command == 'update_dish':
            return self.admin_handler.update_dish(data)
        elif command == 'delete_dish':
            return self.admin_handler.delete_dish(data)
        elif command == 'view_dishes':
            return self.admin_handler.view_dishes()
        else:
            return {'status': 'error', 'message': 'Unknown command'}

    def authenticate(self, username, password):
        query = "SELECT role FROM users WHERE username = %s AND password = %s"
        result = self.db.fetchone(query, (username, password))
        if result:
            return {'status': 'success', 'role': result[0]}
        else:
            return {'status': 'error', 'message': 'Invalid credentials'}

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler_thread.start()

if __name__ == '__main__':
    server = Server()
    server.run()
