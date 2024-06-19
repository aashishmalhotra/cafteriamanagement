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

    def add_user(self, username, password, role):
        return self.send_command('add_user', {'username': username, 'password': password, 'role': role})

    def add_dish(self, dish_name, price):
        return self.send_command('add_dish', {'dish_name': dish_name, 'price': price})

    def update_dish(self, dish_id, new_price):
        return self.send_command('update_dish', {'dish_id': dish_id, 'new_price': new_price})

    def delete_dish(self, dish_id):
        return self.send_command('delete_dish', {'dish_id': dish_id})

    def send_notification(self, message):
        return self.send_command('send_notification', {'message': message})

    def get_feedback(self):
        return self.send_command('get_feedback', {})

    def rollout_menu(self, menu_items):
        return self.send_command('rollout_menu', {'menu_items': menu_items})

    def give_feedback(self, feedback):
        return self.send_command('give_feedback', {'feedback': feedback})

    def see_notification(self):
        return self.send_command('see_notification', {})

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
