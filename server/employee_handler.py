class EmployeeHandler:
    def __init__(self, db_connection):
        self.db_obj = db_connection
        self.db_cursor = self.db_obj.db_cursor
        self.db_connection = self.db_obj.db_connection

    def view_menu(self):
        try:
            query = "SELECT item_id, item_name, meal_type, availability FROM food"
            self.db_cursor.execute(query)
            dishes = self.db_cursor.fetchall()
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def provide_feedback(self, data):
        item_name = data.get('item_name')
        qty = data.get('qty')
        quality = data.get('quality')
        vfm = data.get('vfm')
        comments = data.get('comments')

        if not item_name or not qty or not quality or not vfm or not comments:
            return {'status': 'error', 'message': 'Provide all details for a food item'}

        try:
            query = "SELECT item_id FROM food WHERE item_name = %s"
            self.db_cursor.execute(query, (item_name,))
            result = self.db_cursor.fetchone()

            if not result:
                return {'status': 'error', 'message': 'Item name not found'}

            item_id = result[0]

            query = """INSERT INTO feedback (item_id, qty, quality, vfm, comments) 
                        VALUES (%s, %s, %s, %s, %s)"""
            self.db_cursor.execute(query, (item_id, qty, quality, vfm, comments))
            self.db_connection.commit()
            return {'status': 'success', 'message': 'Feedback submitted'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    def vote_item(self, data):
        item_id = data.get('item_id')
        vote = data.get('vote')
        if not item_id or not vote:
            return {'status': 'error', 'message': 'Invalid data'}

        query = "INSERT INTO vote (item_id, vote) VALUES (%s, %s)"
        self.db_cursor.execute(query, (item_id, vote))
        self.db_connection.commit()
        return {'status': 'success', 'message': 'Vote recorded'}

    def next_day_menu(self):
        query = """SELECT f.* FROM food f
                    JOIN vote v ON f.item_id = v.item_id
                    WHERE v.is_selected = 1"""
        self.db_cursor.execute(query)
        dishes = self.db_cursor.fetchall()
        dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
        print("Next Day menu")
        return {'dishes': dishes_list}
