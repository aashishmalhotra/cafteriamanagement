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
            host="localhost",
            user="your_mysql_username",
            password="your_mysql_password",
            database="company"
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
        elif command == 'add_user' and data.get('role') == 'admin':
            return self.add_user(data['username'], data['password'], data['role'])
        elif command == 'add_dish' and data.get('role') == 'admin':
            return self.add_dish(data['dish_name'], data['price'])
        elif command == 'update_dish' and data.get('role') == 'admin':
            return self.update_dish(data['dish_id'], data['new_price'])
        elif command == 'delete_dish' and data.get('role') == 'admin':
            return self.delete_dish(data['dish_id'])
        elif command == 'send_notification' and data.get('role') == 'chef':
            return self.send_notification(data['message'])
        elif command == 'get_feedback' and data.get('role') == 'chef':
            return self.get_feedback()
        elif command == 'rollout_menu' and data.get('role') == 'chef':
            return self.rollout_menu(data['menu_items'])
        elif command == 'give_feedback' and data.get('role') == 'employee':
            return self.give_feedback(data['feedback'])
        elif command == 'see_notification' and data.get('role') == 'employee':
            return self.see_notification()
        else:
            return {'status': 'error', 'message': 'Unauthorized or unknown command'}

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = self.cursor.fetchone()
        if user:
            return {'status': 'success', 'message': 'Authenticated', 'role': user['role']}
        else:
            return {'status': 'error', 'message': 'Invalid credentials'}

    def add_user(self, username, password, role):
        try:
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            self.db.commit()
            return {'status': 'success', 'message': f'User {username} added with role {role}'}
        except mysql.connector.Error as err:
            return {'status': 'error', 'message': f"Failed to add user: {err}"}

    def add_dish(self, dish_name, price):
        try:
            self.cursor.execute("INSERT INTO dishes (dish_name, price) VALUES (%s, %s)", (dish_name, price))
            self.db.commit()
            return {'status': 'success', 'message': f'Dish {dish_name} added with price {price}'}
        except mysql.connector.Error as err:
            return {'status': 'error', 'message': f"Failed to add dish: {err}"}

    def update_dish(self, dish_id, new_price):
        try:
            self.cursor.execute("UPDATE dishes SET price = %s WHERE id = %s", (new_price, dish_id))
            self.db.commit()
            if self.cursor.rowcount > 0:
                return {'status': 'success', 'message': f'Dish with ID {dish_id} updated to price {new_price}'}
            else:
                return {'status': 'error', 'message': f'Dish with ID {dish_id} not found'}
        except mysql.connector.Error as err:
            return {'status': 'error', 'message': f"Failed to update dish: {err}"}

    def delete_dish(self, dish_id):
        try:
            self.cursor.execute("DELETE FROM dishes WHERE id = %s", (dish_id,))
            self.db.commit()
            if self.cursor.rowcount > 0:
                return {'status': 'success', 'message': f'Dish with ID {dish_id} deleted'}
            else:
                return {'status': 'error', 'message': f'Dish with ID {dish_id} not found'}
        except mysql.connector.Error as err:
            return {'status': 'error', 'message': f"Failed to delete dish: {err}"}

    def send_notification(self, message):
        # Logic to send notification to all employees
        return {'status': 'success', 'message': f'Notification sent: {message}'}

    def get_feedback(self):
        # Logic to retrieve feedback for food from employees
        feedback_data = []  # Placeholder for actual feedback retrieval
        return {'status': 'success', 'feedback': feedback_data}

    def rollout_menu(self, menu_items):
        # Logic to update menu items for the next cycle
        return {'status': 'success', 'message': f'Menu rolled out with items: {menu_items}'}

    def give_feedback(self, feedback):
        # Logic to store feedback provided by employee
        return {'status': 'success', 'message': 'Feedback received and stored'}

    def see_notification(self):
        # Logic to retrieve notifications for the employee
        notifications = []  # Placeholder for actual notification retrieval
        return {'status': 'success', 'notifications': notifications}

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler_thread.start()

if __name__ == '__main__':
    server = Server()
    server.run()
