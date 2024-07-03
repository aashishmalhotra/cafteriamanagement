import datetime
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
            # self.db_connection.commit()
            return {'status': 'success', 'message': 'Notification added successfully'}
        except Exception as e:
            print(f"Error adding notification: {str(e)}")
            return {'status': 'error', 'message': str(e)}
