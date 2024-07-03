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
        print('inside client send_command')
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
            print("Admin commands: add_dish, update_dish, delete_dish, view_dishes, add_notification,view_discard_menu, exit")
            command = input("Enter command: ").strip().lower()

            if command == 'exit':
                break

            elif command in ['add_dish', 'update_dish', 'delete_dish']:
                item_name = input("Enter item name: ")
                meal_type = input("Enter meal type: ")
                availability = input("Enter availability (True/False): ").strip().lower() == 'true'
                data = {'item_name': item_name, 'meal_type': meal_type, 'availability': availability}

                if command in ['update_dish', 'delete_dish']:
                    item_id = int(input("Enter item ID: "))
                    data['item_id'] = item_id

                response = self.send_command(command, data)
                print("Server response:", response)

            elif command == 'view_dishes':
                response = self.send_command(command, {})
                print("Server response:", response)
                for dish in response.get('dishes', []):
                    print(dish)

            elif command == 'add_notification':
                data = str(input("Enter message to be sent as notification: "))
                response = self.send_command('add_notification', data)
                print("Server Response", response)

            # elif command == 'view_discard_menu':
            #     response = self.send_command('view_discard_menu',{})
            #     print(response)
            elif command == 'view_discard_menu':
                response = self.send_command('view_discard_menu', {})

                if response['status'] != 'success':
                    print(response['message'])
                else:
                    discard_items = response['message']
                    if not discard_items:
                        print("No items to discard.")
                        continue

                    for item in discard_items:
                        print(
                            f"Item ID: {item['item_id']}, Item Name: {item['item_name']}")

                    while True:
                        print("\nOptions:")
                        print("1. Remove a food item from the menu")
                        print("2. Get detailed feedback on a food item")
                        print("3. Exit")

                        choice = input("Enter your choice: ").strip()

                        # if choice == '1':
                        #     item_id = input("Enter the item ID to remove: ").strip()
                        #     # self.remove_food_item(item_id)
                        #     self.send_command('remove_food_item',item_id)

                        if choice == '1':
                            item_id = input("Enter the item ID to remove: ").strip()
                            data = {'item_id': item_id}
                            response = self.send_command('remove_food_item', data)
                            print("Server response:", response)


                        elif choice == '2':
                            item_id = input("Enter the item ID to get detailed feedback: ").strip()
                            questions = []

                            for i in range(3):
                                question = input(f"Enter question {i + 1}: ")
                                questions.append(question)

                            data = {'item_id': item_id, 'questions': questions}
                            response = self.send_command('get_detailed_feedback', data)
                            print("Server response:", response)

                        elif choice == '3':
                            break

                        else:
                            print("Invalid choice. Please try again.")

            else:
                print("Invalid command")

    def handle_chef_commands(self):
        while True:
            print("Chef commands: view_menu, view_recommendation,add_notification, voting_results, choose_final_menu, exit")
            command = input("Enter command: ").strip().lower()

            if command == 'exit':
                break

            elif command == 'view_menu':
                response = self.send_command('view_menu', {})
                print("Current menu:", response)
                for dish in response.get('dishes', []):
                    print(dish)

            elif command == 'view_recommendation':
                num_items = int(input("Enter number of items to recommend: ").strip())
                response = self.send_command('view_recommendation', {'num_items': num_items})
                print("Recommended dishes:")
                print("In response",response)
                for dish in response.get('dishes', []):
                    print(dish)

            elif command == 'add_notification':
                data = str(input("Enter message to be sent as notification: "))
                response = self.send_command('add_notification',data)
                print("Server Response",response)

            elif command == 'voting_results':
                response = self.send_command('voting_results', {})
                print("Voting results:", response)
                for result in response.get('results', []):
                    print(result)

            elif command == 'choose_final_menu':
                item_ids = input("Enter item IDs for final menu (comma-separated): ")
                item_ids = [int(item_id.strip()) for item_id in item_ids.split(',')]
                response = self.send_command('choose_final_menu', {'item_ids': item_ids})
                print("Server response:", response)

            else:
                print("Invalid command")

    def handle_employee_commands(self):
        while True:
            print("Employee commands: view_menu, vote_item, provide_feedback, next_day_menu,show_notification, send_detailed_feedback, exit")
            command = input("Enter command: ").strip().lower()

            if command == 'exit':
                break

            elif command == 'view_menu':
                response = self.send_command('view_menu', {})
                print("Current menu:")
                for dish in response.get('dishes', []):
                    print(dish)

            elif command == 'provide_feedback':
                item_name = input("Enter item name: ")
                qty = int(input("Enter quantity: "))
                quality = int(input("Enter quality: "))
                vfm = int(input("Enter value for money (vfm): "))
                comments = input("Enter comments: ")

                data = {'item_name': item_name, 'qty': qty, 'quality': quality, 'vfm': vfm, 'comments': comments}
                response = self.send_command('provide_feedback', data)
                print("Server response:", response)

            elif command == 'vote_item':
                item_id = int(input("Enter item ID to vote: "))
                vote = input("Enter your vote: ")
                data = {'item_id': item_id, 'vote': vote}
                response = self.send_command(command, data)
                print("Server response:", response)

            elif command == 'next_day_menu':
                response = self.send_command('next_day_menu', {})
                print("Next day's menu:")
                for dish in response.get('dishes', []):
                    print(dish)

            elif command == 'show_notification':
                user_name = str(input("Enter your username: "))
                data = {'user_name': user_name}
                response = self.send_command('show_notification',data)
                print("Today's Notification:")
                for notification in response.get('messages_list',[]):
                    print(notification)

            elif command == 'provide_feedback':
                item_id = int(input("Enter item ID to provide feedback: "))
                rating = float(input("Enter rating (1-5): "))
                comment = input("Enter your comments: ")
                data = {'item_id': item_id, 'rating': rating, 'comment': comment}
                response = self.send_command('provide_feedback', data)
                print("Server response:", response)

            elif command == 'send_detailed_feedback':
                response = self.send_command('show_pending_feedback', {})
                if response['status'] != 'success':
                    print(response['message'])
                else:
                    questions = response.get('questions', [])
                    if not questions:
                        print("No pending feedback questions.")
                        continue

                    feedback_data = []
                    for question in questions:
                        print(f"Item: {question['item_name']} (ID: {question['item_id']})")
                        print(f"Question {question['question_id']}: {question['question']}")
                        answer = input("Enter your answer: ")
                        feedback_data.append({
                            'item_id': question['item_id'],
                            'question_id': question['question_id'],
                            'answer': answer
                        })

                    response = self.send_command('send_detailed_feedback', {'feedback': feedback_data})
                    print("Server response:", response)

            else:
                print("Command not found in client")

    def run(self):
        self.connect()
        username = input("Username: ")
        password = input("Password: ")
        if self.authenticate(username, password):
            if self.role == 'admin':
                self.handle_admin_commands()
            elif self.role == 'chef':
                self.handle_chef_commands()
            elif self.role == 'employee':
                self.handle_employee_commands()
        self.sock.close()


if __name__ == '__main__':
    client = Client()
    client.run()
