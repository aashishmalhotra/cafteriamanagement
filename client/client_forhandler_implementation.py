import socket
import json

class Client:
    def __init__(self, host='localhost', port=8889):
        self.host = host
        self.port = port
        self.role = None

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
            self.role = response['role']
            print(f"Authenticated successfully as {self.role}")
            return True
        else:
            print("Authentication failed:", response['message'])
            return False

    def handle_admin_commands(self):
        while True:
            print("Admin commands: add_dish, update_dish, delete_dish, view_dishes, exit")
            command = input("Enter command: ").strip().lower()

            if command == 'exit':
                break

            if command in ['add_dish', 'update_dish', 'delete_dish']:
                item_name = input("Enter item name: ")
                meal_type = input("Enter meal type: ")
                availability = input("Enter availability (True/False): ").strip().lower() == 'true'
                data = {'item_name': item_name, 'meal_type': meal_type, 'availability': availability}

                if command == 'update_dish' or command == 'delete_dish':
                    item_id = int(input("Enter item ID: "))
                    data['item_id'] = item_id

                response = self.send_command(command, data)
                print("Server response:", response)

            elif command == 'view_dishes':
                response = self.send_command(command, {})
                print("Server response:", response)

            else:
                print("Invalid command")

    def run(self):
        self.connect()
        username = input("Username: ")
        password = input("Password: ")
        if self.authenticate(username, password):
            if self.role == 'admin':
                self.handle_admin_commands()
            # Handle other roles here...

if __name__ == '__main__':
    client = Client()
    client.run()
