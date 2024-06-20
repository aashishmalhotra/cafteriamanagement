import socket
import threading
import json
import mysql.connector

class Server:
    def __init__(self, host='127.0.0.1', port=8889):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        # Connect to MySQL database
        self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Admin@!2345",
            database="fd"
        )
        self.db_cursor = self.db_connection.cursor()

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
            return self.add_dish(data)
        elif command == 'update_dish':
            return self.update_dish(data)
        elif command == 'delete_dish':
            return self.delete_dish(data)
        elif command == 'view_dishes':
            return self.view_dishes(data)
        else:
            return {'status': 'error', 'message': 'Unknown command'}

    def authenticate(self, username, password):
        query = "SELECT role FROM users WHERE username = %s AND password = %s"
        self.db_cursor.execute(query, (username, password))
        result = self.db_cursor.fetchone()
        if result:
            return {'status': 'success', 'role': result[0]}
        else:
            return {'status': 'error', 'message': 'Invalid credentials'}

    def add_dish(self, data):
        try:
            query = "INSERT INTO food (item_name, meal_type, availability) VALUES (%s, %s, %s)"
            self.db_cursor.execute(query, (data['item_name'], data['meal_type'], data['availability']))
            self.db_connection.commit()
            return {'status': 'success', 'message': 'Item added successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_dish(self, data):
        try:
            query = "UPDATE food SET item_name = %s, meal_type = %s, availability = %s WHERE item_id = %s"
            self.db_cursor.execute(query, (data['item_name'], data['meal_type'], data['availability'], data['item_id']))
            self.db_connection.commit()
            print("in try")
            return {'status': 'success', 'message': 'Item updated successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def delete_dish(self, data):
        try:
            query = "DELETE FROM food WHERE item_id = %s"
            self.db_cursor.execute(query, (data['item_id'],))
            self.db_connection.commit()
            return {'status': 'success', 'message': 'Dish deleted successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def view_dishes(self, data):
        try:
            query = "SELECT item_id, item_name, meal_type, availability FROM food"
            self.db_cursor.execute(query)
            dishes = self.db_cursor.fetchall()
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler_thread.start()

if __name__ == '__main__':
    server = Server()
    server.run()
