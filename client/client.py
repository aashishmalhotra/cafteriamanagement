import socket
import json

class Client:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print("Connected to server")

    def send_command(self, command, data):
        message = json.dumps({'command': command, 'data': data})
        self.sock.sendall(message.encode())
        response = self.sock.recv(4096).decode()
        return json.loads(response)

    def authenticate(self, username, password):
        response = self.send_command('authenticate', {'username': username, 'password': password})
        if response['status'] == 'success':
            print(f"Authenticated successfully as {response['role']}")
            return True
        else:
            print("Authentication failed:", response['message'])
            return False

    def handle_employee_commands(self):
        while True:
            command = input("Enter command: ")
            if command == 'exit':
                break
            data = input("Enter data: ")
            response = self.send_command(command, {'data': data})
            print("Server response:", response)

    def run(self):
        self.connect()
        username = input("Username: ")
        password = input("Password: ")
        if self.authenticate(username, password):
            self.handle_employee_commands()
        self.sock.close()

if __name__ == '__main__':
    client = Client()
    client.run()
