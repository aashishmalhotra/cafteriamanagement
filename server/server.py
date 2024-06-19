import socket
import threading
import json
import mysql.connector

class Server:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Admin@!2345",
            database="fd"
        )
        self.cursor = self.db.cursor(dictionary=True)

    def handle_client(self, client_socket):
        try:
            while True:
                message = client_socket.recv(4096).decode()
                if not message:
                    break
                data = json.loads(message)
                command = data.get('command')
                response = self.route_command(command, data.get('data'))
                client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def route_command(self, command, data):
        if command == 'authenticate':
            return self.authenticate_user(data['username'], data['password'])
        else:
            return {'status': 'error', 'message': 'Unknown command'}

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = self.cursor.fetchone()
        if user:
            return {'status': 'success', 'message': 'Authenticated', 'role': user['role']}
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
