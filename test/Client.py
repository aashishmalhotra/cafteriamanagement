import socket
import json

class Client:
    def __init__(self, host='localhost', port=9998):
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
        response = self.sock.recv(1024).decode()
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
            print("Admin commands: add_user, add_dish, update_dish, delete_dish, exit")
            command = input("Enter command: ").strip().lower()

            if command == 'exit':
                break

            if command == 'add_dish':
                try:
                    item_name = input("Enter item name: ")
                    meal_type = input("Enter meal type: ")
                    availability = input("Enter availability (True/False): ")

                    data = {'item_name': item_name, 'meal_type': meal_type, 'availability': availability}

                    response = self.send_command('add_dish',data )

                    if response['status'] == 'success':
                        print("Dish added successfully")
                    else:
                        print(response['status'])

                except json.JSONDecodeError:
                    print("Invalid data format")
                    continue
                except Exception as e:
                    print(f"Error: {e}")

            else:
                print("Invalid command")

    def run(self):
        self.connect()
        username = input("Username: ")
        password = input("Password: ")
        if self.authenticate(username, password):
            if self.role == 'admin':
                self.handle_admin_commands()
            # elif self.role == 'chef':
            #     self.handle_chef_commands()
            # elif self.role == 'employee':
            #     self.handle_employee_commands()

if __name__ == '__main__':
    client = Client()
    client.run()
