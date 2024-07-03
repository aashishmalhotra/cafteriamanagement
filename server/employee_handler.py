import datetime

class EmployeeHandler:
    def __init__(self, db_connection):
        self.db = db_connection

    def view_menu(self):
        try:
            query = "SELECT item_id, item_name, meal_type, availability FROM food"
            dishes = self.db.fetchall(query)
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
            result = self.db.fetchone(query, (item_name,))

            if not result:
                return {'status': 'error', 'message': 'Item name not found in database'}

            item_id = result[0]

            query = """INSERT INTO feedback (item_id, item_name, qty, quality, vfm, comments) 
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            self.db.execute(query, (item_id, item_name, qty, quality, vfm, comments))
            return {'status': 'success', 'message': 'Feedback submitted'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def vote_item(self, data):
        item_id = data.get('item_id')
        vote = data.get('vote')

        if not item_id or not vote:
            return {'status': 'error', 'message': 'Invalid data'}

        try:
            query = "INSERT INTO vote (item_id, vote) VALUES (%s, %s)"
            self.db.execute(query, (item_id, vote))
            return {'status': 'success', 'message': 'Vote recorded'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def next_day_menu(self):
        try:
            query = """SELECT f.* FROM food f
                       JOIN vote v ON f.item_id = v.item_id
                       WHERE v.is_selected = 1"""
            dishes = self.db.fetchall(query)
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def show_notification(self, data):
        # user_id = data.get('user_id')
        username = data.get('user_name')

        try:
            query = "SELECT id FROM users WHERE username = %s"
            result = self.db.fetchone(query, (username,))

            if not result:
                return {'status': 'error', 'message': 'User not found'}

            user_id = result[0]

            print("inside try")
            # query = "SELECT message FROM notification WHERE date = %s"
            # today_date = datetime.date.today()
            # date_tuple = (today_date.year, today_date.month, today_date.day)
            # messages = self.db.fetchall(query, (date_tuple,))
            # print(messages)

            today_date = datetime.date.today()
            date_str = today_date.strftime('%Y-%m-%d')

            query = "SELECT message FROM notification WHERE date = %s"
            messages = self.db.fetchall(query, (date_str,))

            messages_list = [{'message': message[0]} for message in messages]

            return {'status': 'success', 'messages': messages_list}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # def show_notification(self):
    #     try:
    #         current_date = datetime.datetime.now().date()
    #         query = "SELECT message FROM notification WHERE DATE(date) = %s"
    #         messages = self.db.fetchall(query, (current_date,))
    #
    #         if messages:
    #             # Track which user has seen the notifications
    #             for message in messages:
    #                 track_query = "INSERT INTO notification_view (user_id, date) VALUES (%s, %s)"
    #                 self.db.execute(track_query, (self.user_id, datetime.datetime.now()))
    #
    #             print("Got the notifications")
    #             return {'status': 'success', 'messages': [msg[0] for msg in messages]}
    #         else:
    #             return {'status': 'success', 'messages': []}
    #
    #     except Exception as e:
    #         return {'status': 'error', 'message': str(e)}

    # def show_notification(self):
    #     current_time = datetime.datetime.now()
    #     query = """SELECT message
    #                 FROM notification
    #                 where date = %s"""
    #     message = self.db.execute(query, current_time)
    #     print("Got the notification")
    #     return {'message': message}


# class EmployeeHandler:
#     def __init__(self, db_connection):
#         self.db_obj = db_connection
#         self.db_cursor = self.db_obj.db_cursor
#         self.db_connection = self.db_obj.db_connection
#
#     def view_menu(self):
#         try:
#             query = "SELECT item_id, item_name, meal_type, availability FROM food"
#             self.db_cursor.execute(query)
#             dishes = self.db_cursor.fetchall()
#             dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
#             return {'status': 'success', 'dishes': dishes_list}
#         except Exception as e:
#             return {'status': 'error', 'message': str(e)}
#
#     def provide_feedback(self, data):
#         item_name = data.get('item_name')
#         qty = data.get('qty')
#         quality = data.get('quality')
#         vfm = data.get('vfm')
#         comments = data.get('comments')
#
#         if not item_name or not qty or not quality or not vfm or not comments:
#             return {'status': 'error', 'message': 'Provide all details for a food item'}
#
#         try:
#             query = "SELECT item_id FROM food WHERE item_name = %s"
#             self.db_cursor.execute(query, (item_name,))
#             result = self.db_cursor.fetchone()
#
#             if not result:
#                 return {'status': 'error', 'message': 'Item name not found in database'}
#
#             print(result)
#             item_id = result[0]
#
#             query = """INSERT INTO feedback (item_id, item_name,qty, quality, vfm, comments)
#                         VALUES (%s, %s, %s, %s, %s, %s)"""
#             self.db_cursor.execute(query, (item_id,item_name, qty, quality, vfm, comments))
#             self.db_connection.commit()
#             return {'status': 'success', 'message': 'Feedback submitted'}
#         except Exception as e:
#             return {'status': 'error', 'message': str(e)}
#     def vote_item(self, data):
#         item_id = data.get('item_id')
#         vote = data.get('vote')
#         if not item_id or not vote:
#             return {'status': 'error', 'message': 'Invalid data'}
#
#         query = "INSERT INTO vote (item_id, vote) VALUES (%s, %s)"
#         self.db_cursor.execute(query, (item_id, vote))
#         self.db_connection.commit()
#         return {'status': 'success', 'message': 'Vote recorded'}
#
#     def next_day_menu(self):
#         query = """SELECT f.* FROM food f
#                     JOIN vote v ON f.item_id = v.item_id
#                     WHERE v.is_selected = 1"""
#         self.db_cursor.execute(query)
#         dishes = self.db_cursor.fetchall()
#         dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
#         print("Next Day menu")
#         return {'dishes': dishes_list}
#
#     def show_notifications(self):
#         current_time = datetime.datetime.now()
#         query = """SELECT
#                     FROM notification
#                     where date = %s"""
#         self.
