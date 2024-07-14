import datetime
from server.databases import admin_queries


class AdminHandler:
    def __init__(self, db):
        self.db = db

    def add_dish(self, data):
        try:
            query = admin_queries.insert_food()
            self.db.execute(query, (data['item_name'], data['meal_type'], data['availability']))
            return {'status': 'success', 'message': 'Item added successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_dish(self, data):
        try:
            query = admin_queries.update_food()
            self.db.execute(query, (data['item_name'], data['meal_type'], data['availability'], data['item_id']))
            return {'status': 'success', 'message': 'Item updated successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def delete_dish(self, data):
        try:
            query = admin_queries.delete_food()
            self.db.execute(query, (data['item_id'],))
            return {'status': 'success', 'message': 'Dish deleted successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def view_dishes(self):
        try:
            query = admin_queries.get_food_details()
            dishes = self.db.fetchall(query)
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for
                           dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def add_notification(self, message):
        try:
            current_time = datetime.datetime.now()
            query = admin_queries.insert_notification()
            self.db.execute(query, (message, current_time))
            return {'status': 'success', 'message': 'Notification added successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def view_discard_menu(self):
        try:
            query = admin_queries.get_low_rated_items()
            self.db.db_cursor.execute(query)
            low_rated_items = self.db.db_cursor.fetchall()

            discard_items = [{'item_id': item[0], 'item_name': item[1]} for item in low_rated_items]

            return {'status': 'success', 'message': discard_items}
        except Exception as e:
            return {'status': 'error in discard menu', 'message': str(e)}

    def handle_discard_options(self):
        response = self.view_discard_menu()
        if response['status'] != 'success':
            print(response['message'])
            return

        discard_items = response['message']
        if not discard_items:
            print("No items to discard.")
            return

        for item in discard_items:
            print(f"Item ID: {item['item_id']}, Item Name: {item['item_name']}")

        while True:
            print("\nOptions:")
            print("1. Remove a food item from the menu")
            print("2. Get detailed feedback on a food item")
            print("3. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                item_id = input("Enter the item ID to remove: ").strip()
                response = self.remove_food_item({'item_id': item_id})
                print(response['message'])

            elif choice == '2':
                item_id = input("Enter the item ID to get detailed feedback: ").strip()
                self.get_detailed_feedback({'item_id': item_id})

            elif choice == '3':
                break

            else:
                print("Invalid choice. Please try again.")

    def remove_food_item(self, data):
        try:
            query_delete_feedback = admin_queries.delete_feedback_by_item()
            item_id = data['item_id']
            self.db.execute(query_delete_feedback, (item_id,))

            query_delete_food = admin_queries.delete_food()
            self.db.execute(query_delete_food, (item_id,))

            return {'status': 'success', 'message': 'Food item removed successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_detailed_feedback(self, data):
        try:
            item_id = data.get('item_id')
            questions = data.get('questions')

            for question in questions:
                query = admin_queries.insert_detailed_feedback()
                self.db.execute(query, (item_id, question))

            return {'status': 'success', 'message': 'Detailed feedback request sent successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def store_feedback(self, item_id, question, answer):
        try:
            query = admin_queries.insert_detailed_feedback_with_answer()
            self.db.execute(query, (item_id, question, answer))
            return {'status': 'success', 'message': 'Feedback stored successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
