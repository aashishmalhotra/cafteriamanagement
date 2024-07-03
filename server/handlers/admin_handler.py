import datetime
import decimal
class AdminHandler:
    def __init__(self, db):
        self.db = db

    def add_dish(self, data):
        try:
            query = "INSERT INTO food (item_name, meal_type,availability) VALUES (%s, %s, %s)"
            self.db.execute(query, (data['item_name'], data['meal_type'], data['availability']))
            return {'status': 'success', 'message': 'Item added successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_dish(self, data):
        try:
            query = "UPDATE food SET item_name = %s, meal_type = %s, availability = %s WHERE item_id = %s"
            self.db.execute(query, (data['item_name'], data['meal_type'] , data['availability'], data['item_id']))
            return {'status': 'success', 'message': 'Item updated successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def delete_dish(self, data):
        print('in delete')
        try:
            query = "DELETE FROM food WHERE item_id = %s"
            self.db.execute(query, (data['item_id'],))
            return {'status': 'success', 'message': 'Dish deleted successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def view_dishes(self):
        try:
            query = "SELECT item_id, item_name, meal_type, availability FROM food"
            dishes = self.db.fetchall(query)
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def add_notification(self, message):
        try:
            current_time = datetime.datetime.now()
            query = "INSERT INTO notification (message, date) VALUES (%s, %s)"
            self.db.execute(query, (message, current_time))
            # self.db.commit()
            return {'status': 'success', 'message': 'Notification added successfully'}
        except Exception as e:
            print(f"Error adding notification: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def view_discard_menu(self):
        try:
            # Query to get the average rating of each item
            query_ratings = """
                            SELECT f.item_id, f.item_name,
                            AVG((COALESCE(fb.qty, 0) + COALESCE(fb.quality, 0) + COALESCE(fb.vfm, 0)) / 5) AS avg_rating
                            FROM food f
                            JOIN feedback fb ON f.item_id = fb.item_id
                            GROUP BY f.item_id
                            HAVING avg_rating < 2;
                            """
            self.db.db_cursor.execute(query_ratings)
            low_rated_items = self.db.db_cursor.fetchall()
            print(low_rated_items)
            # Query to get the comments for each item
            # query_comments = """
            #     SELECT f.item_id, f.item_name, fb.comments
            #     FROM food f
            #     JOIN feedback fb ON f.item_id = fb.item_id
            # """
            # self.db.execute(query_comments)
            # comments = self.db.fetchall()

            # Analyze comments for negative sentiments
            # negative_keywords = ["tasteless", "extremely bad experience", "very poor","over cooked"]
            discard_items = [
                {
                    'item_id': item[0],
                    'item_name': item[1],
                    # 'avg_rating': float(item[2]) if isinstance(item[2], decimal.Decimal) else item[2]
                }
                for item in low_rated_items
            ]
            # for item in low_rated_items:
            #     item_id, item_name, avg_rating = item
            #     # for comment in comments:
            #     #     if comment[0] == item_id:
            #     #         analysis = TextBlob(comment[2])
            #     #         if any(keyword in analysis.lower() for keyword in negative_keywords):
            #     discard_items.append({'item_id': item_id, 'item_name': item_name, 'avg_rating': avg_rating})

            print("inside discard menu")
            return {'status': 'success', 'message':     discard_items}

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
            print(f"Item ID: {item['item_id']}, Item Name: {item['item_name']}, Average Rating: {item['avg_rating']}")

        while True:
            print("\nOptions:")
            print("1. Remove a food item from the menu")
            print("2. Get detailed feedback on a food item")
            print("3. Exit")

            choice = input("Enter your choice: ").strip()

            # if choice == '1':
            #     item_id = input("Enter the item ID to remove: ").strip()
            #     self.remove_food_item(item_id)

            if choice == '1':
                item_id = input("Enter the item ID to remove: ").strip()
                response = self.remove_food_item(item_id)
                print(response['message'])

            elif choice == '2':
                item_id = input("Enter the item ID to get detailed feedback: ").strip()
                self.get_detailed_feedback(item_id)

            elif choice == '3':
                break

            else:
                print("Invalid choice. Please try again.")

    def remove_food_item(self, data):
        try:
            # Delete associated feedback first
            print('inside remove')
            query_delete_feedback = "DELETE FROM feedback WHERE item_id = %s"
            item_id = data['item_id']
            print("remove food item_id",item_id)
            self.db.execute(query_delete_feedback, (item_id,))

            # Then delete the food item
            query_delete_food = "DELETE FROM food WHERE item_id = %s"
            self.db.execute(query_delete_food, (item_id,))

            # self.db.commit()
            print("Commited delete")
            return {'status': 'success', 'message': 'Food item  removed successfully'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_detailed_feedback(self, data):
        try:
            item_id = data.get('item_id')
            questions = data.get('questions')
            print("inserting questions")

            # Insert each question into the detailed_feedback table
            for idx, question in enumerate(questions, 1):
                query = "INSERT INTO detailed_feedback (item_id,question) VALUES (%s, %s)"
                print('Query being made')
                self.db.execute(query, (item_id, question))

            # self.db.db_conn.commit()
            print("inserted questions by chef")
            return {'status': 'success', 'message': 'Detailed feedback request sent successfully'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def store_feedback(self, item_id, question, answer):
        try:
            query = "INSERT INTO detailed_feedback (item_id, question, answer) VALUES (%s, %s, %s)"
            self.db.db_cursor.execute(query, (item_id, question, answer))
            self.db.db_connection.commit()
            print("Feedback stored successfully.")
        except Exception as e:
            print(f"Error storing feedback: {e}")

