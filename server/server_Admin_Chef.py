import socket
import threading
import json
from databases.database import Database
from handlers.admin_handler import AdminHandler
from chef_handler import ChefHandler
from employee_handler import EmployeeHandler
from recomm2 import RecommendationSystem
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
        self.chef_handler = ChefHandler(self.db)
        self.employee_handler = EmployeeHandler(self.db)
        self.recommendation_system = RecommendationSystem(self.db)


    def handle_client(self, client_socket):
        try:
            while True:
                message = client_socket.recv(4096).decode()
                if not message:
                    break
                print(f"Received message: {message}")
                data = json.loads(message)
                command = data['command']
                response = self.route_command(command, data['data'])
                response_message = json.dumps(response)
                print(f"Sending response: {response_message}")
                client_socket.sendall(response_message.encode())
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
        elif command == 'add_notification':
            return self.admin_handler.add_notification(data)
        elif command == 'view_discard_menu':
            return self.admin_handler.view_discard_menu()
        elif command == 'remove_food_item':
            return self.admin_handler.remove_food_item(data)
        elif command == 'get_detailed_feedback':
            return self.admin_handler.get_detailed_feedback((data))

        elif command == 'view_menu':
            return self.chef_handler.view_menu()
        elif command == 'choose_final_menu':
            return self.chef_handler.choose_final_menu(data)
        elif command == 'view_recommendation':
            return self.chef_handler.view_recommendation(data)
        elif command == 'add_notification':
            return self.chef_handler.add_notification(data)
        elif command == 'voting_results':
            return self.chef_handler.voting_results()

        elif command == 'view_menu':
            return self.employee_handler.view_menu()
        elif command == 'provide_feedback':
            return self.employee_handler.provide_feedback(data)
        elif command == 'vote_item':
            return self.employee_handler.vote_item(data)
        elif command == 'next_day_menu':
            return self.employee_handler.next_day_menu()
        elif command == 'show_notification':
            return self.employee_handler.show_notification(data)
        elif command == 'send_detailed_feedback':
            return self.employee_handler
        else:
            return {'status': 'error', 'message': 'Unknown command'}

    def authenticate(self, username, password):
        query = "SELECT role FROM users WHERE username = %s AND password = %s"
        self.db.db_cursor.execute(query, (username, password))
        result = self.db.db_cursor.fetchone()
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
