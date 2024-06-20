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
        command_functions = {
            'add_dish': self.add_dish,
            'update_dish': self.update_dish,
            'delete_dish': self.delete_dish
        }

        while True:
            print("Admin commands: add_user, add_dish, update_dish, delete_dish, exit")
            command = input("Enter command: ").strip().lower()

            if command == 'exit':
                break
            elif command in command_functions:
                try:
                    command_functions[command]()
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Invalid command")

    def add_dish(self):
        item_name = input("Enter item name: ").strip()
        meal_type = input("Enter meal type: ").strip()
        availability = input("Enter availability (True/False): ").strip().lower() == 'true'

        data = {'item_name': item_name, 'meal_type': meal_type, 'availability': availability}
        response = self.send_command('add_dish', data)

        if response['status'] == 'success':
            print("Dish added successfully")
        else:
            print(response['message'])

    def update_dish(self):
        dish_id = input("Enter dish ID: ").strip()
        item_name = input("Enter new item name: ").strip()
        meal_type = input("Enter new meal type: ").strip()
        availability = input("Enter new availability (True/False): ").strip().lower() == 'true'

        data = {'id': dish_id, 'item_name': item_name, 'meal_type': meal_type, 'availability': availability}
        response = self.send_command('update_dish', data)

        if response['status'] == 'success':
            print("Dish updated successfully")
        else:
            print(response['message'])

    def delete_dish(self):
        dish_id = input("Enter dish ID: ").strip()

        data = {'id': dish_id}
        response = self.send_command('delete_dish', data)

        if response['status'] == 'success':
            print("Dish deleted successfully")
        else:
            print(response['message'])

    def run(self):
        self.connect()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if self.authenticate(username, password):
            if self.role == 'admin':
                self.handle_admin_commands()
            # elif self.role == 'chef':
            #     self.handle_chef_commands()
            # elif self.role == 'employee':
            #     self.handle_employee_commands()
        self.sock.close()

if __name__ == '__main__':
    client = Client()
    client.run()
